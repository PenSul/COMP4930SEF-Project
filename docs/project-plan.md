# Project methodology and milestones

## Foundation

Use one report notebook, small typed Python helpers, a public Git repository,
and reproducible environments. Native Windows supports team development and
photo preparation; the Legion's WSL2 environment provides NVIDIA GPU training.
The repository starts with an unexecuted notebook outline. Record actual
experiments as each task is implemented.

## Task 1 — CIFAR-100 animals and people (20%)

Use exactly the appendix's 50 fine-grained classes, remapping to integer labels
0–49. Split the 25,000 development images into a fixed stratified 20,000 training
and 5,000 validation set. Reserve the official 5,000 test images for final evaluation.

Compare exactly three architectures:

1. ImageNet-pretrained MobileNet V1 with a new classification head.
2. A compact custom CNN trained from scratch.
3. ImageNet-pretrained EfficientNetV2B0 with a new classification head.

Use compact global-average-pooling heads, modest training-only augmentation,
staged fine-tuning, early stopping and best-checkpoint saving. MobileNet expects
pixels scaled to [-1, 1]; EfficientNetV2's built-in preprocessing expects [0, 255].
Keep pretrained BatchNorm statistics stable when fine-tuning and recompile after
changing trainability. Resize per batch to limit host memory. Use GPU mixed
precision with a float32 classifier output after verifying the training device.

Use a bounded development budget, then compare locked configurations across seeds
42, 43 and 44 on the same split. Mean validation accuracy is the primary selection
measure; report macro-F1, per-class errors, confusion matrices, top-5 accuracy,
parameters, runtime and variability. Use macro-F1, then fewer parameters to resolve
exact ties. Explain the reasons for adjustments and outcomes using actual evidence.

The final evaluation uses the seed-42 best-validation checkpoint of the selected
configuration, with its preprocessing and label mapping preserved. Keep the test
set out of model selection. Evaluate that locked checkpoint once and retain it
for Task 2. Lectures and labs serve as references; the project brief and the
experimental design determine the workflow.

## Task 2 — team-collected photographs (35%)

Follow the [collection guide](data-collection.md). Choose the five classes together,
target about 600 original photographs, cross-review labels, and use an object-group
split. Adapt the actual Task 1 winning checkpoint, replacing its classifier and
comparing frozen-feature and fine-tuned stages with one controlled augmentation
experiment. Report validation results and at least 25 labelled predictions.
Analyse errors by class, collector and capture condition where sample counts allow.

## Task 3 — AG News topic classification (35%)

Use AG News's four classes: World, Sports, Business, Sci/Tech. The original dataset
has 120,000 training and 7,600 test examples. At this stage, add a pinned
`tensorflow-datasets` dependency and load `ag_news_subset:1.0.0`, explicitly
combining title and description. Document the source, research-use terms, original
counts and any exclusions from duplicate auditing. Preserve the official test set;
split development data with stratification and keep duplicate groups together.

Use one text CNN: TextVectorization, embedding, parallel Conv1D widths 3/4/5,
global max pooling, dropout and a four-class classifier. Start with a 20,000-token
vocabulary, 128-token sequences and 128-dimensional embeddings. Fit vocabulary
on training data only. Document cleaning, unknown words and truncation, compare
64- and 128-token inputs, and analyse actual classification errors. Perform a final
held-out evaluation after configuration selection.

## Reporting and submission (video: 10%)

The notebook includes title/group/member information, introduction, Task 1,
recommendation and final evaluation, Task 2, Task 3, and references. Preserve
execution outputs, figures and required implementation code. Supply full names
and 8-digit IDs when the group confirms them.

Prepare one separate document containing the declaration, workload allocation
and individual summaries, plus a 5–8 minute video with every member presenting.
Submit these three deliverables through OLE; separate photo files are excluded
from the OLE submission. Target 3 December 2026, ahead of the official deadline
of 4 December, 23:59 Hong Kong time. Verify the submission status after uploading.

The brief assumes equal contributions. Any agreed unequal allocation requires
notification to Kayley by 19 November, 23:59, with all members CC'd and consenting.

## Sources

- COMP 4930SEF Project, Autumn 2026, supplied course brief.
- Chip Huyen, *Designing Machine Learning Systems*, O'Reilly, 2022, chapters 4–6.
- [Keras transfer learning and fine-tuning](https://keras.io/guides/transfer_learning/).
- Howard et al., [MobileNets](https://arxiv.org/abs/1704.04861), 2017.
- Tan and Le, [EfficientNetV2](https://proceedings.mlr.press/v139/tan21a.html), 2021.
- [TensorFlow Datasets: AG News](https://www.tensorflow.org/datasets/catalog/ag_news_subset).
- Zhang et al., [Character-level Convolutional Networks for Text Classification](https://arxiv.org/abs/1509.01626), 2015 (AG News benchmark).
- Kim, [Convolutional Neural Networks for Sentence Classification](https://aclanthology.org/D14-1181/), 2014.
