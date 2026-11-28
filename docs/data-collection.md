# Task 2: collecting our container dataset

We will classify one visible drink container into one of five classes. Each of
us takes and labels our own photographs across **all five classes**. Our target
is **200 usable images per member, 600 altogether**. The counts below are our
collection plan; record the actual totals after review.

## 1. The five agreed classes

Use these exact folder names. The order in
[`classes.json`](../data/task2/classes.json) defines the future integer labels.
These are the labelling rules for this dataset.

| ID | Folder / label | What belongs here | Useful variety |
| --- | --- | --- | --- |
| 0 | `mug` | A ceramic or stoneware drinking mug with a handle. | Straight or rounded sides; small or large; different colours, patterns and handle shapes. |
| 1 | `glass_bottle` | A glass bottle made to hold a drink, with a recognisable bottle neck and mouth. | Glass-bottled soy milk, milk, soda, juice or water; different shapes, colours and sizes. |
| 2 | `plastic_bottle` | A plastic bottle made to hold a drink, with a recognisable bottle neck and mouth. | PET bottled water, soft drinks, tea or juice; reusable plastic water or sports bottles. |
| 3 | `aluminium_can` | An intact aluminium beverage can with its normal body and rim visible. | Regular and slim cans, different sizes and printed designs. |
| 4 | `drink_carton` | A paperboard beverage carton, including its usual plastic/foil layers, with flat panels and visible edges. | Milk, soy drink, juice or tea cartons; different sizes, box shapes or gable tops. |

### Which bottles count?

Check what the bottle was originally made to hold, then check the **body
material** on the actual item. A glass water bottle with a plastic cap goes in
`glass_bottle`. Empty drink bottles count, and changing the contents keeps the
original label and design group.

| Bottle you have | Collection decision |
| --- | --- |
| A disposable PET water bottle or a reusable plastic sports bottle with a short, wide neck | Use `plastic_bottle`. A short neck is enough if you can see where the body narrows to the mouth. The cap can stay on. |
| A glass soy milk bottle or a vintage glass soda bottle | Use `glass_bottle` when you can identify its original use for drinks. Age and fill level do not change the class. |
| A glass cooking-oil, soy sauce or cooking vinegar bottle, even if someone has refilled it with water | Leave it out. Its original use was for cooking or seasoning. |
| A decorative or vintage bottle of unknown use, a glass jar, or a straight-sided travel tumbler with a lid as wide as its body | Leave it out. We need an identifiable drink bottle. Metal water flasks also fall outside both bottle classes. |

For bottle photos, keep the neck, mouth or cap, body and base in frame. For
the other classes, keep the can rim, carton edges or mug handle visible.
Set aside drinking glasses, paper or plastic cups, food tins, food boxes and
crushed containers. Discuss uncertain items before taking a full batch.

## 2. What we mean by different designs

A **design** is a visibly different version within one class. For example, a
small plain white mug, a tall blue mug, a rounded patterned mug and a wide mug
with a different handle give us useful variety within `mug`.

- A water bottle, a soft-drink bottle, a juice bottle and a tea bottle can supply
  four designs when their shape, size or packaging visibly differs.
- Two identical bottles of the same product and size share one design group.
- A new angle, background, photographer, cap position or fill level keeps the
  original object's group ID.
- The same brand can have several designs. Compare the actual shape, size and
  packaging; use one group for identical or near-identical variants. If two items
  would look almost identical in a photo, reuse the group ID. A capacity difference
  alone may be invisible after resizing the images.

All views of one physical object, and matching designs photographed by different
members, stay together later.
This lets validation measure performance on containers whose designs were held
out of training. See the [grouped evaluation guidance](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data).

## 3. Plan the objects before taking hundreds of photos

Use this allocation as the starting target:

| Class | Images per member | Suggested objects per member | Usable photos per object | Team images |
| --- | ---: | ---: | ---: | ---: |
| Mug | 40 | 4 different designs | 10 | 120 |
| Glass drink bottle | 40 | 4 different designs | 10 | 120 |
| Plastic bottle | 40 | 4 different designs | 10 | 120 |
| Aluminium can | 40 | 4 different designs | 10 | 120 |
| Drink carton | 40 | 4 different designs | 10 | 120 |
| **Total** | **200** | **20 objects** | | **600** |

Four designs per class per member is a practical target. Each member's access to
those objects still needs checking. Use objects you already have or can borrow;
empty, clean containers in their usual shape are suitable.

Record real objects in the shared
[`object-groups.md`](../data/task2/object-groups.md) register. Add a short visual
description and the members who can access them. Share a reference photo in the
group chat when a written description leaves doubt about whether two items match.
The register starts empty; fill it with the objects we actually find.

For a new design, use an ID such as `m1_mug_01`, `m2_glass_bottle_02` or
`m3_drink_carton_01`. The prefix identifies who first registered it. Reuse the
existing ID whenever someone else photographs the same object or matching design.
For example, M2's photos of M1's mug still use `m1_mug_01`; their collector is M2.

**Sharing objects:** borrow items when one member has fewer examples. Everyone
still takes their own photographs in their own capture sessions. Count distinct
group IDs across the whole team: a design shared by all three members contributes
one independent group. Aim for about 12 distinct groups per class where accessible.
If the inventory has only a few designs in a class, discuss how to find more before
the main shoot and agree any adjustment to the allocation.

## 4. Run a small pilot first

Start with approximately **ten images per class across the team**: M1 can take
four per class, and M2 and M3 three each, giving 50 pilot images. Use a few of the
registered objects and include different views and lighting conditions.

Review the pilot together at full size and as small thumbnails. Check that the
class remains obvious and the object is sharp. Try both a glass bottle and a
plastic water bottle on the same surface and in the same light. At thumbnail
size, check whether glare hides the neck, body or base. Resolve uncertain labels
and group IDs before the main shoot. Accepted pilot photos count
towards each member's 200 and the object's ten-photo target.

## 5. Set up the phone and scene

1. Clean the camera lens. Use the rear camera's normal **Photo** mode at **1x**.
   Keep the original full-resolution files; JPEG or PNG is accepted by our importer.
   Export HEIC/HEIF files as JPEG before import, preserving the camera originals.
2. Use normal camera processing consistently. Turn off portrait blur, beauty or
   artistic filters, stickers and added watermarks. Move the phone to change
   framing; avoid digital zoom and screenshots of photos.
3. Place one target container on a stable surface. Keep its complete outline and
   identifying features visible, with a margin around it. For most shots, let it
   occupy roughly **60–80% of the image height**; include a few wider views.
4. Tap the container to focus, hold the phone steady and take one deliberate shot.
   Check it immediately. Keep the clearest attempt for that view when retaking.
5. Start with soft window light or outdoor shade. For clear bottles, choose a
   background that makes the outline visible. Move the object or camera when glare
   hides a can's rim, a label, or a large area of the body.
6. Use ordinary backgrounds: a desk, kitchen counter, plain cloth or uncluttered
   shelf. Keep faces, personal information and other target containers outside the
   frame. Mild everyday clutter and natural shadows are useful when the object
   remains easy to identify.

Both portrait and landscape images are acceptable. Keep the object in focus and
leave its outline clear. Avoid straight-down views that reduce a cup or can to a
similar-looking circle, and extreme close-ups that hide the type of container.

## 6. Ten useful photographs of each object

Use **two capture sessions**, with five selected views in each. A session is one
capture occasion; the second can be later the same day or on another day after
setting up again. Change the background and lighting between sessions. Within
one session, keep the session ID while changing the view or surface.

The table is a shooting checklist. Adjust the exact angle to keep the object's
identifying features visible, especially a mug's handle.

| Shot | Session | How to take it |
| --- | --- | --- |
| 1 | `session_01` | Front view near the object's height, whole container visible. |
| 2 | `session_01` | Three-quarter view from the left. |
| 3 | `session_01` | Three-quarter view from the right. |
| 4 | `session_01` | Turn the object to show another face or the back; retain enough shape to identify it. |
| 5 | `session_01` | Mild view from above, showing both the opening/top and the body. |
| 6 | `session_02` | Front view on the second background in a different light condition. |
| 7 | `session_02` | A new three-quarter view, slightly closer, with the full outline still inside the frame. |
| 8 | `session_02` | A mildly lower camera angle; keep the body and its distinctive features visible. |
| 9 | `session_02` | A wider view, roughly 40–60% of image height, with some surrounding context. |
| 10 | `session_02` | Place the object off-centre and choose a distinct view. A hand holding its lower edge is optional if most of the object stays visible. |

Move the camera or rotate/reposition the object between captures. Select distinct
views from the session. Ten nearly identical burst frames give little
additional coverage. Take replacements when needed to reach ten usable photos.

**Use each setup across all five classes.** For example, photograph some mugs,
glass drink bottles, plastic bottles, cans and cartons on the same desk in
window light. Repeat all five on the second surface under room light. Distribute optional handheld
shots across classes too. This reduces opportunities for the model to associate
a class with one background, hand, light condition or photographer. Background
shortcuts are a known source of poor generalisation ([Geirhos et al.](https://arxiv.org/abs/2004.07780)).

Keep ordinary packaging and printed labels intact, and include different sides
of the object. Create additional training variations through augmentation later;
our collected-image count consists of distinct camera photographs.

## 7. Put originals in labelled folders

Each member keeps a source folder **outside the Git repository**:

```text
C:\Users\Alice\Pictures\COMP4930-photos\
  mug\
    m2_mug_01\
      session_01\
        IMG_1001.jpg
        IMG_1002.jpg
      session_02\
        IMG_1041.jpg
  glass_bottle\
    m2_glass_bottle_01\
      session_01\
        IMG_1101.jpg
  plastic_bottle\
    m2_plastic_bottle_01\
      session_01\
        IMG_1201.jpg
  aluminium_can\
    m2_aluminium_can_01\
      session_01\
        IMG_1301.jpg
  drink_carton\
    m2_drink_carton_01\
      session_01\
        IMG_1401.jpg
```

The nesting is **class / object group / session / photograph**. Use the registered
group IDs, including another member's prefix when sharing a design. Session names
are local to the photographer: M1 and M2 can both have a `session_01`.

Keep camera filenames. Folder IDs use lowercase letters, digits and underscores,
start with a letter, and have at most 40 characters. Group descriptions, capture
notes and rejected photos belong outside this import folder. Move rejected
originals into a separate sibling folder such as `COMP4930-photos-excluded` and
keep a short exclusion log there with filename, reason and reviewer.

## 8. Review, prepare and upload

First inspect the originals. Retake or set aside images with an uncertain class,
poor focus, heavy glare, a hidden identifying feature, a cropped object or almost
the same view as another chosen image. Keep a clear photo even when the background
or angle is somewhat challenging. Review collection quality before training.

Pull the latest main branch and follow the full
[photo contribution workflow](team-setup.md#7-prepare-and-upload-task-2-photos).
For M2, the preparation command is:

```powershell
mise exec -- python scripts/prepare_photos.py --member M2 --source "$HOME\Pictures\COMP4930-photos"
```

It preserves originals, corrects orientation, and creates RGB JPEGs with the
longest edge at most 1,024 pixels and quality 90. Outputs go to
`data/task2/images/M2/<class_name>/` and `data/task2/manifests/M2.csv`.
Leave the prepared JPEGs unedited so their recorded checksums remain valid.

Before the first commit, fill the capture annotations in the CSV, keeping its
header and saving as UTF-8. Record `reviewer` after the other member confirms
their review, then commit and push that update to the same contribution branch:

| Field | What to enter | Example |
| --- | --- | --- |
| `lighting` | The actual light condition for that photo. | `window_daylight`, `room_light`, `outdoor_shade` |
| `background` | A short, consistent description of the surface or setting. | `wooden_desk`, `kitchen_counter`, `plain_cloth` |
| `notes` | Relevant details, such as handheld capture or mild glare. | `held at base; neck and outline visible` |
| `reviewer` | The other member's ID, filled after they check the photo and record. | `M1` |

Values above are examples; record what actually happened. Additional annotation
columns are preserved by the importer. Keep the path, class, collector, group,
session and checksum fields consistent with the imported photo.

Check your per-class counts in PowerShell:

```powershell
Import-Csv data/task2/manifests/M2.csv | Group-Object class_name | Select-Object Name, Count
```

Target 40 accepted rows per class for each member. Compare the group IDs against
the shared object register as well. A useful review rotation is M1 reviewing M2,
M2 reviewing M3, and M3 reviewing M1. The reviewer checks images at full size and
as a thumbnail grid, then checks labels, group IDs and capture annotations before
PenSul reviews and merges the pull request under the
[team development workflow](development-workflow.md). Windows File Explorer's
large-icon view is sufficient for the thumbnail pass; open individual photos
to assess sharpness.

The importer detects exact source-file duplicates against the manifests available
locally. Review visually similar shots and identical designs across members too.
Pull the latest merged contributions before preparing a batch, and reconcile
overlapping designs or duplicates from concurrent branches before merging.

**Correcting an imported mistake:** imports append records, so moving a source
photo out of the import folder leaves its existing dataset record in place.
On your contribution branch:

1. Copy the affected row's lighting, background and still-relevant notes or custom
   annotations before removing it. Keep this temporary record outside the source
   import folder.
2. Move or relabel the original, and remove only its affected generated JPEG and
   matching CSV row together. Preserve the other rows and their annotations.
3. Rerun preparation for corrected photos. The replacement row starts with empty
   annotations: restore the saved capture information, update any details affected
   by the correction, and leave `reviewer` empty until the correction is checked.
4. Update the object register if needed, then stage the removals and new files with
   `git add -A -- data/task2/images/M2 data/task2/manifests/M2.csv data/task2/object-groups.md`.
   Commit and push the update to the existing contribution branch for review.
   After confirmation, record the reviewer's ID and commit/push that CSV update too.

For a rejected photo with no replacement, retain its exclusion record outside
the import folder. Coordinate shared-group changes across members.

## 9. The later training/validation split

Keep the collected files in the member folders; the notebook will assign a fixed
split from the manifests after review. Target **75% training / 25% validation**,
with every class and collector represented in both where the groups allow it.
All photos of one physical object or matching design stay in one split across
members and sessions. Split choices use metadata and coverage before training.

With 12 equal-sized, independent groups per class, nine training groups and three
validation groups would give approximately 90/30 images per class and 450/150
overall. Shared designs change the available group counts and sizes; document
the actual split and preserve group separation when adjusting the ratio.

Labels come from `class_name` and the ordered class list. Apply random augmentation
only to training images. Adapt the actual selected Task 1 checkpoint and show 25
fixed validation predictions, five per class, with actual and predicted labels.
Select those displayed examples using a recorded rule before inspecting prediction
correctness, and analyse additional errors separately.

## References

- Chip Huyen, *Designing Machine Learning Systems* (2022), chapters 4–6:
  labelling, data provenance and evaluation by data subset.
- Gebru et al., [Datasheets for Datasets](https://arxiv.org/abs/1803.09010):
  documenting dataset composition and collection procedures.
- Geirhos et al., [Shortcut Learning in Deep Neural Networks](https://arxiv.org/abs/2004.07780):
  why convenient visual cues can undermine generalisation.
- scikit-learn, [Cross-validation iterators for grouped data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data):
  keeping related observations together during evaluation.
