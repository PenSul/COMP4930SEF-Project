"""Prepare one member's photographs and merge their collection records."""

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

MEMBERS = ("M1", "M2", "M3")
FIELDS = (
    "relative_path",
    "class_name",
    "collector_id",
    "object_group_id",
    "session_id",
    "source_sha256",
    "output_sha256",
    "lighting",
    "background",
    "reviewer",
    "notes",
)
CORE_FIELDS = FIELDS[:7]
RESERVED = {"con", "prn", "aux", "nul"} | {
    f"{prefix}{number}" for prefix in ("com", "lpt") for number in range(1, 10)
}
IGNORED_FILES = {".ds_store", "thumbs.db", "desktop.ini"}
Row = dict[str, str]


def checksum(content: bytes) -> str:
    """Return the full SHA-256 digest used in collection records."""
    return hashlib.sha256(content).hexdigest()


def validate_identifier(value: str) -> None:
    """Require short, portable folder identifiers shared by all collectors."""
    if not re.fullmatch(r"[a-z][a-z0-9_]{0,39}", value) or value in RESERVED:
        raise ValueError(
            f"Invalid identifier {value!r}: use lowercase letters, digits and "
            "underscores, starting with a letter (maximum 40 characters)."
        )


def load_classes(data_dir: Path) -> list[str]:
    """Load the team's agreed class order; an empty list means still undecided."""
    path = data_dir / "classes.json"
    classes = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(classes, list) or len(classes) < 2:
        raise ValueError("Agree on the classes and fill data/task2/classes.json first.")
    if any(not isinstance(name, str) for name in classes):
        raise ValueError("classes.json must contain a list of class-name strings.")
    for name in classes:
        validate_identifier(name)
    if len(set(classes)) != len(classes):
        raise ValueError("classes.json contains duplicate class names.")
    return classes


def relative_output(row: Row) -> str:
    """Use content-based names so additional batches never renumber old photos."""
    name = (
        f"{row['object_group_id']}_{row['session_id']}_{row['source_sha256'][:16]}.jpg"
    )
    return (
        Path("data/task2/images") / row["collector_id"] / row["class_name"] / name
    ).as_posix()


def destination(project_dir: Path, relative_path: str) -> Path:
    path = project_dir / relative_path
    if not path.resolve().is_relative_to(project_dir):
        raise ValueError(f"Output path escapes the project: {relative_path}")
    return path


def read_manifests(project_dir: Path, classes: list[str]) -> list[Row]:
    """Check existing records before an import can extend the shared dataset."""
    rows: list[Row] = []
    seen_sources: set[str] = set()
    seen_paths: set[str] = set()
    group_classes: dict[str, str] = {}
    for member in MEMBERS:
        manifest = project_dir / "data/task2/manifests" / f"{member}.csv"
        if not manifest.exists():
            continue
        with manifest.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if not set(CORE_FIELDS).issubset(reader.fieldnames or []):
                raise ValueError(f"Missing required columns in {manifest.name}.")
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(f"Malformed CSV row in {manifest.name}.")
                if row["collector_id"] != member or row["class_name"] not in classes:
                    raise ValueError(f"Invalid member or class in {manifest.name}.")
                for field in ("class_name", "object_group_id", "session_id"):
                    validate_identifier(row[field])
                for field in ("source_sha256", "output_sha256"):
                    if not re.fullmatch(r"[0-9a-f]{64}", row[field]):
                        raise ValueError(f"Invalid checksum in {manifest.name}.")
                if row["relative_path"] != relative_output(row):
                    raise ValueError(f"Unexpected image path in {manifest.name}.")
                if row["source_sha256"] in seen_sources:
                    raise ValueError("Duplicate source image in existing manifests.")
                if row["relative_path"].casefold() in seen_paths:
                    raise ValueError("Case-insensitive output filename collision.")
                previous_class = group_classes.setdefault(
                    row["object_group_id"], row["class_name"]
                )
                if previous_class != row["class_name"]:
                    raise ValueError("An object group has conflicting class labels.")
                image = destination(project_dir, row["relative_path"])
                if (
                    not image.is_file()
                    or checksum(image.read_bytes()) != row["output_sha256"]
                ):
                    raise ValueError(f"Missing or changed imported image: {image}")
                seen_sources.add(row["source_sha256"])
                seen_paths.add(row["relative_path"].casefold())
                rows.append(row)
    return rows


def jpeg_copy(content: bytes, source: Path) -> bytes:
    """Apply camera orientation before resizing; retain no source EXIF metadata."""
    try:
        with Image.open(io.BytesIO(content)) as original:
            if getattr(original, "n_frames", 1) != 1:
                raise ValueError(f"Use a single still photograph: {source}")
            image = ImageOps.exif_transpose(original).convert("RGB")
            image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            output = io.BytesIO()
            image.save(output, format="JPEG", quality=90, optimize=True, exif=b"")
            return output.getvalue()
    except (OSError, Image.DecompressionBombError) as error:
        raise ValueError(f"Cannot decode photograph: {source}") from error


def write_manifest(path: Path, rows: list[Row]) -> None:
    """Replace the CSV atomically, including any additional hand-written columns."""
    fields = list(dict.fromkeys([*FIELDS, *(key for row in rows for key in row)]))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False
        ) as stream:
            temporary = Path(stream.name)
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def prepare_photos(source_dir: Path, member: str, project_dir: Path) -> int:
    """Preflight a complete batch, then append new photos to one member's records.

    Originals live outside the repository under class/group/session folders.
    All decoding and collision checks happen before writes. Existing records
    retain review fields; identical reimports are a no-op. An interrupted write
    can be retried because matching orphaned JPEGs can be adopted safely.
    """
    project_dir = project_dir.resolve()
    source_dir = source_dir.resolve()
    if member not in MEMBERS:
        raise ValueError("Member must be M1, M2 or M3.")
    if not source_dir.is_dir() or source_dir.is_relative_to(project_dir):
        raise ValueError("Choose a folder of originals outside the project directory.")
    data_dir = project_dir / "data/task2"
    classes = load_classes(data_dir)
    existing = read_manifests(project_dir, classes)
    by_source = {row["source_sha256"]: row for row in existing}
    groups = {row["object_group_id"]: row["class_name"] for row in existing}
    seen_sources: set[str] = set()
    seen_paths = {row["relative_path"].casefold() for row in existing}
    pending: list[tuple[Row, bytes]] = []

    for source in sorted(source_dir.rglob("*")):
        if source.is_symlink():
            raise ValueError(f"Use original files, not symbolic links: {source}")
        if not source.is_file() or source.name.casefold() in IGNORED_FILES:
            continue
        parts = source.relative_to(source_dir).parts
        if len(parts) != 4:
            raise ValueError(f"Expected class/object_group/session/photo: {source}")
        class_name, group, session, _ = parts
        for identifier in (class_name, group, session):
            validate_identifier(identifier)
        if class_name not in classes:
            raise ValueError(f"Unknown class {class_name!r}; check classes.json.")
        if source.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            raise ValueError(f"Export photos as JPEG or PNG before importing: {source}")
        if groups.setdefault(group, class_name) != class_name:
            raise ValueError(f"Object group {group!r} already has another class.")

        content = source.read_bytes()
        source_hash = checksum(content)
        if source_hash in seen_sources:
            raise ValueError(f"Duplicate photograph in this batch: {source}")
        seen_sources.add(source_hash)
        row = dict.fromkeys(FIELDS, "")
        row.update(
            class_name=class_name,
            collector_id=member,
            object_group_id=group,
            session_id=session,
            source_sha256=source_hash,
        )
        row["relative_path"] = relative_output(row)
        previous = by_source.get(source_hash)
        if previous is not None:
            identity = ("collector_id", "class_name", "object_group_id", "session_id")
            if any(previous[field] != row[field] for field in identity):
                raise ValueError(
                    "Duplicate image already recorded with different collection "
                    f"details: {source}"
                )
            continue
        if row["relative_path"].casefold() in seen_paths:
            raise ValueError(f"Output filename collision for {source}.")
        seen_paths.add(row["relative_path"].casefold())
        jpeg = jpeg_copy(content, source)
        row["output_sha256"] = checksum(jpeg)
        output = destination(project_dir, row["relative_path"])
        if output.exists() and (
            not output.is_file()
            or checksum(output.read_bytes()) != row["output_sha256"]
        ):
            raise ValueError(f"Existing output has conflicting contents: {output}")
        pending.append((row, jpeg))

    if not seen_sources:
        raise ValueError("No photographs found in the source folder.")
    if not pending:
        return 0
    for row, jpeg in pending:
        output = destination(project_dir, row["relative_path"])
        output.parent.mkdir(parents=True, exist_ok=True)
        if not output.exists():
            with output.open("xb") as stream:
                stream.write(jpeg)
    member_rows = [row for row in existing if row["collector_id"] == member]
    member_rows.extend(row for row, _ in pending)
    member_rows.sort(key=lambda row: row["relative_path"])
    write_manifest(data_dir / "manifests" / f"{member}.csv", member_rows)
    return len(pending)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--member", choices=MEMBERS, required=True)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args()
    project_dir = Path(__file__).resolve().parents[1]
    try:
        count = prepare_photos(args.source, args.member, project_dir)
    except (OSError, ValueError) as error:
        print(f"Import failed: {error}", file=sys.stderr)
        return 1
    print(f"Added {count} photographs for {args.member}.")
    print(f"Images: data/task2/images/{args.member}/")
    print(f"Manifest: data/task2/manifests/{args.member}.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
