"""Exercise photo imports with temporary, synthetic image fixtures."""

import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts.prepare_photos import prepare_photos


class PhotoImportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project"
        self.source = self.root / "camera photos"
        self.data = self.project / "data" / "task2"
        self.data.mkdir(parents=True)
        (self.data / "classes.json").write_text('["mug", "can"]', encoding="utf-8")

    def photo(
        self,
        relative: str = "mug/object_01/session_01/IMG_001.png",
        size: tuple[int, int] = (40, 20),
        color: str = "red",
    ) -> Path:
        path = self.source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", size, color).save(path)
        return path

    def rows(self, member: str = "M2") -> list[dict[str, str]]:
        path = self.data / "manifests" / f"{member}.csv"
        with path.open(encoding="utf-8", newline="") as stream:
            return list(csv.DictReader(stream))

    def import_photos(self, member: str = "M2") -> int:
        return prepare_photos(self.source, member, self.project)

    def test_resizes_and_records_identity_without_changing_original(self) -> None:
        original = self.photo(size=(1600, 800))
        before = original.read_bytes()
        self.assertEqual(self.import_photos(), 1)
        row = self.rows()[0]
        output = self.project / row["relative_path"]
        with Image.open(output) as image:
            self.assertEqual(image.size, (1024, 512))
            self.assertEqual(image.mode, "RGB")
            self.assertEqual(image.format, "JPEG")
        self.assertEqual(original.read_bytes(), before)
        self.assertEqual(row["source_sha256"], hashlib.sha256(before).hexdigest())
        self.assertEqual(
            row["output_sha256"], hashlib.sha256(output.read_bytes()).hexdigest()
        )
        self.assertEqual(row["class_name"], "mug")
        self.assertEqual(row["collector_id"], "M2")
        self.assertEqual(row["object_group_id"], "object_01")
        self.assertEqual(row["session_id"], "session_01")
        self.assertNotIn("\\", row["relative_path"])

    def test_exif_orientation_is_applied_and_metadata_removed(self) -> None:
        original = self.photo("mug/object_01/session_01/rotated.jpg", (40, 20))
        exif = Image.Exif()
        exif[274] = 6
        exif[315] = "Camera owner"
        Image.new("RGB", (40, 20), "blue").save(original, exif=exif)
        self.import_photos()
        with Image.open(self.project / self.rows()[0]["relative_path"]) as image:
            self.assertEqual(image.size, (20, 40))
            self.assertFalse(image.getexif())

    def test_small_rgba_photo_is_converted_without_upscaling(self) -> None:
        original = self.photo()
        Image.new("RGBA", (30, 15), (0, 255, 0, 255)).save(original)
        self.import_photos()
        with Image.open(self.project / self.rows()[0]["relative_path"]) as image:
            self.assertEqual(image.size, (30, 15))
            self.assertEqual(image.mode, "RGB")

    def test_repeat_import_keeps_bytes_and_manual_review_fields(self) -> None:
        self.photo()
        self.import_photos()
        manifest = self.data / "manifests" / "M2.csv"
        rows = self.rows()
        rows[0]["reviewer"] = "M3"
        rows[0]["lighting"] = "window daylight"
        rows[0]["extra_note"] = "Checked with the collector"
        with manifest.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        before = manifest.read_bytes()
        image = self.project / rows[0]["relative_path"]
        image_before = image.read_bytes()
        self.assertEqual(self.import_photos(), 0)
        self.assertEqual(manifest.read_bytes(), before)
        self.assertEqual(image.read_bytes(), image_before)

    def test_new_batch_retains_previous_rows_and_annotations(self) -> None:
        old = self.photo()
        self.import_photos()
        manifest = self.data / "manifests" / "M2.csv"
        previous = self.rows()
        previous[0]["reviewer"] = "M1"
        previous[0]["extra_note"] = "Retain this after the next batch"
        with manifest.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(previous[0]))
            writer.writeheader()
            writer.writerows(previous)
        old.unlink()
        self.photo("can/object_02/session_02/another.png", color="blue")
        self.assertEqual(self.import_photos(), 1)
        self.assertEqual(len(self.rows()), 2)
        self.assertEqual({row["class_name"] for row in self.rows()}, {"mug", "can"})
        retained = next(row for row in self.rows() if row["class_name"] == "mug")
        self.assertEqual(retained["reviewer"], "M1")
        self.assertEqual(retained["extra_note"], previous[0]["extra_note"])
        for row in self.rows():
            self.assertTrue((self.project / row["relative_path"]).is_file())

    def test_unselected_classes_fail_before_writing(self) -> None:
        (self.data / "classes.json").write_text("[]", encoding="utf-8")
        self.photo()
        with self.assertRaisesRegex(ValueError, "classes.json"):
            self.import_photos()
        self.assertFalse((self.data / "images").exists())

    def test_unknown_class_and_bad_layout_are_rejected(self) -> None:
        for relative in ("cup/object_01/session_01/a.png", "mug/a.png"):
            with self.subTest(relative=relative):
                path = self.photo(relative)
                with self.assertRaises(ValueError):
                    self.import_photos()
                path.unlink()
                self.assertFalse((self.data / "images").exists())

    def test_corrupt_later_photo_prevents_partial_batch(self) -> None:
        self.photo()
        broken = self.photo("mug/object_01/session_01/z.png")
        broken.write_bytes(b"not an image")
        with self.assertRaises(ValueError):
            self.import_photos()
        self.assertFalse((self.data / "images").exists())
        self.assertFalse((self.data / "manifests").exists())

    def test_unsupported_camera_format_has_actionable_error(self) -> None:
        path = self.source / "mug/object_01/session_01/image.heic"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"heic placeholder")
        with self.assertRaisesRegex(ValueError, "JPEG|PNG"):
            self.import_photos()

    def test_empty_source_invalid_member_and_inside_repo_are_rejected(self) -> None:
        self.source.mkdir()
        with self.assertRaises(ValueError):
            self.import_photos()
        self.photo()
        with self.assertRaises(ValueError):
            self.import_photos("M4")
        with self.assertRaises(ValueError):
            prepare_photos(self.project, "M2", self.project)

    def test_windows_unsafe_or_case_ambiguous_ids_are_rejected(self) -> None:
        for group in ("Object_01", "bad group"):
            with self.subTest(group=group):
                path = self.photo(f"mug/{group}/session_01/a.png")
                with self.assertRaises(ValueError):
                    self.import_photos()
                path.unlink()

    def test_camera_names_with_different_contents_stay_distinct(self) -> None:
        self.photo("mug/object_01/session_01/IMG.JPG", color="red")
        # Use distinct names on Windows; output names derive from content hashes.
        self.photo("mug/object_01/session_01/img_copy.jpg", color="blue")
        self.assertEqual(self.import_photos(), 2)
        paths = [row["relative_path"].casefold() for row in self.rows()]
        self.assertEqual(len(set(paths)), 2)

    def test_duplicate_originals_are_rejected(self) -> None:
        original = self.photo()
        duplicate = original.with_name("copy.png")
        duplicate.write_bytes(original.read_bytes())
        with self.assertRaisesRegex(ValueError, "[Dd]uplicate"):
            self.import_photos()

    def test_duplicate_from_another_member_is_rejected(self) -> None:
        self.photo()
        self.import_photos("M1")
        with self.assertRaisesRegex(ValueError, "[Dd]uplicate"):
            self.import_photos("M2")

    def test_changed_group_and_session_with_same_output_name_is_rejected(self) -> None:
        original = self.photo("mug/object/session_one/image.png")
        self.import_photos()
        manifest = self.data / "manifests" / "M2.csv"
        before = manifest.read_bytes()
        moved = self.source / "mug/object_session/one/image.png"
        moved.parent.mkdir(parents=True)
        original.rename(moved)
        with self.assertRaisesRegex(ValueError, "[Dd]uplicate"):
            self.import_photos()
        self.assertEqual(manifest.read_bytes(), before)

    def test_shared_group_cannot_change_class_between_members(self) -> None:
        old = self.photo()
        self.import_photos("M1")
        old.unlink()
        self.photo("can/object_01/session_01/new.png", color="blue")
        with self.assertRaisesRegex(ValueError, "group"):
            self.import_photos("M2")

    def test_modified_existing_output_is_not_overwritten(self) -> None:
        self.photo()
        self.import_photos()
        output = self.project / self.rows()[0]["relative_path"]
        output.write_bytes(b"changed deliberately")
        with self.assertRaises(ValueError):
            self.import_photos()
        self.assertEqual(output.read_bytes(), b"changed deliberately")

    def test_existing_untracked_output_conflict_is_preserved(self) -> None:
        self.photo()
        self.import_photos()
        output = self.project / self.rows()[0]["relative_path"]
        (self.data / "manifests" / "M2.csv").unlink()
        output.write_bytes(b"conflicting content")
        with self.assertRaises(ValueError):
            self.import_photos()
        self.assertEqual(output.read_bytes(), b"conflicting content")

    def test_interrupted_import_with_matching_image_can_be_recovered(self) -> None:
        self.photo()
        self.import_photos()
        (self.data / "manifests" / "M2.csv").unlink()
        self.assertEqual(self.import_photos(), 1)
        self.assertEqual(len(self.rows()), 1)

    def test_manifest_path_traversal_is_rejected(self) -> None:
        self.photo()
        self.import_photos()
        manifest = self.data / "manifests" / "M2.csv"
        rows = self.rows()
        rows[0]["relative_path"] = "../../outside.jpg"
        with manifest.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaises(ValueError):
            self.import_photos()

    def test_invalid_class_configuration_is_rejected(self) -> None:
        self.photo()
        for classes in (["mug", "mug"], {"classes": ["mug", "can"]}, ["mug", "CON"]):
            with self.subTest(classes=classes):
                (self.data / "classes.json").write_text(
                    json.dumps(classes), encoding="utf-8"
                )
                with self.assertRaises(ValueError):
                    self.import_photos()


if __name__ == "__main__":
    unittest.main()
