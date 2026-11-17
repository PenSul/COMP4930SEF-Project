# Task 2 collection guide

## Decide the classes together

The class list is pending. Choose one proposal and agree on definitions before
the main collection. Set `data/task2/classes.json` to the agreed ordered JSON
list and review that change together. The importer intentionally stops while
the list is empty. The order will define the later model's label mapping.

| Proposal | Five suggested class names | What to check in the pilot |
| --- | --- | --- |
| Containers (preferred) | `mug`, `paper_cup`, `plastic_bottle`, `aluminium_can`, `drink_carton` | Clear boundaries for reusable cups, bottles of different materials, and unusual packaging. |
| Stationery | `wooden_pencil`, `mechanical_pencil`, `ballpoint_pen`, `highlighter`, `marker` | Pens and pencils should remain distinguishable in the photographed view; establish how tips/caps are shown. |

## Collection target

Aim for **600 usable photographs**, approximately **200 per member**, covering
all five classes. A useful allocation is 40 photos per class per member:
four distinct object designs with ten deliberate views of each. Confirm that
these objects are accessible before scheduling the main collection.

Start with ten pilot images per class across the group. Review the class
definitions, visibility and image quality together. Accepted pilot images count
towards the target.

- Every member photographs every class and labels their own contributions.
- Use at least two sessions. Vary backgrounds, light, camera distance and angle.
- Photograph all classes across the chosen backgrounds and lighting conditions.
- Keep one prominent target object visible. Review ambiguous or unusably blurred
  images and record exclusions.
- Take distinct photographs. Preserve the original camera files and avoid burst
  sequences of almost identical frames. All dataset photos are collected by the team.

## Group identifiers and review

Assign object-group identifiers such as `object_017` together. Reuse an identifier
when different members photograph the same object or visually identical designs.
Assign session identifiers such as `session_01` for each member's capture sessions.
Collection records identify both the member and session, so a session number can
be reused by another member.

Arrange originals as `class_name/object_group_id/session_id/photo.jpg` and follow
the [preparation and upload commands](team-setup.md#7-prepare-and-upload-task-2-photos).
The manifest records paths, labels, collectors, groups, sessions and checksums.
Complete its lighting/background fields. Review another member's labels and
enter the reviewer identifier; discuss uncertain labels before merging.

The importer checks exact source-file duplicates across available manifests.
During review, also inspect contact sheets for near-duplicate shots and inconsistent
group identifiers. All members should pull the latest merged manifests before
preparing a batch. Reconcile any duplicates that arrive through simultaneous
contribution branches before accepting the combined dataset.

## Training/validation split

After collection review, create a fixed split targeting **75% training / 25%
validation**, maintaining class coverage and representation from all members.
Keep every object group in one split across members and sessions. Adjust image
counts when needed to honour groups; document the resulting counts and number
of independent groups in each class.

Read labels from the manifest's `class_name` column. The top-level M1/M2/M3 image
directories identify collectors. Apply random augmentation only to training
images. Show 25 fixed validation predictions (five per class), including the
image, actual label and predicted label, and analyse errors separately.

## References

- COMP 4930SEF project brief, Task 2: team collection/labelling, adaptation of the
  recommended Task 1 model, validation and at least 20 displayed predictions.
- Chip Huyen, *Designing Machine Learning Systems* (2022), chapters 4–6:
  labelling, data provenance, group leakage and evaluation by data subset.
- Gebru et al., [Datasheets for Datasets](https://arxiv.org/abs/1803.09010):
  documenting dataset composition and collection procedures.
