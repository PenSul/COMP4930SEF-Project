# Team setup and contribution guide

Use native Windows 10/11 x64 for development and photo uploads. Full training
runs will use the Legion through WSL2 or a cloud GPU. Commands in the Windows
sections below run in **PowerShell**, from the project directory after cloning.

## 1. Install the tools

Open PowerShell and run:

```powershell
winget install --id Git.Git --exact --source winget
winget install --id jdx.mise --exact --source winget
winget install --id GitHub.cli --exact --source winget
winget install --id "Microsoft.VCRedist.2015+.x64" --exact --source winget
```

If `winget` is unavailable, install or update Microsoft's **App Installer** through
the Microsoft Store. Accept the installer prompts. The C++ redistributable supplies
the runtime required by TensorFlow on Windows.

Close and reopen Windows Terminal or PowerShell to load the updated PATH:

```powershell
git --version
mise --version
gh --version
```

Official instructions: [Git](https://git-scm.com/install/windows),
[mise](https://mise.jdx.dev/installing-mise.html),
[GitHub CLI](https://github.com/cli/cli/blob/trunk/docs/install_windows.md),
[TensorFlow](https://www.tensorflow.org/install/pip).

## 2. Set your Git identity and sign in

Create a GitHub account if needed. Use your own name and a verified GitHub email
or the GitHub-provided no-reply email from your account settings:

```powershell
git config --global user.name "Your Name"
git config --global user.email "YOUR_GITHUB_EMAIL"
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

Follow the browser instructions. The repository owner adds both teammates under
**Settings → Collaborators**. Accept that invitation before uploading a branch.
Public read access supports cloning; collaborator write access supports this
guide's upload commands. Check the signed-in account with `gh auth status`.

## 3. Clone the repository

```powershell
New-Item -ItemType Directory -Force "$HOME\Projects"
Set-Location "$HOME\Projects"
git clone https://github.com/PenSul/COMP4930SEF-Project.git Project
Set-Location Project
```

The usual path is `C:\Users\<username>\Projects\Project`. Clone once per computer.
Use `git pull` to update an existing checkout.

## 4. Install Python and dependencies

```powershell
mise trust
mise install
mise exec -- python -m pip install -r requirements-dev.txt
```

Mise installs Python 3.12.15 and creates `.venv`. `mise exec` and `mise run`
automatically select that environment, including on Windows.

Verify it:

```powershell
mise exec -- python --version
mise exec -- python -c "import sys; print(sys.executable)"
mise exec -- python -m pip check
mise exec -- python -c "import tensorflow as tf; print(tf.__version__)"
```

Expect Python 3.12.15, an interpreter inside `.venv\Scripts`, no broken
dependencies, and TensorFlow 2.21.0. Native Windows development uses the CPU.
If a TensorFlow import reports a missing Microsoft runtime DLL, complete the
C++ redistributable installation from step 1 and reopen the terminal.

## 5. Open the report and run checks

```powershell
mise run lab
```

Open `project_report.ipynb`. Stop JupyterLab with Ctrl+C in its terminal when
finished. The initial notebook is a report outline; model training is added
task by task.

Development checks run from another PowerShell window in the project directory:

```powershell
mise run test
mise run lint
mise run typecheck
```

Type checking exports a temporary Python copy of the notebook into `.cache/`.
The notebook remains the source of the report.

## 6. Start a new work session

Commit existing work on its own branch, then update main:

```powershell
git switch main
git pull --ff-only
mise exec -- python -m pip install -r requirements-dev.txt
```

For code work, create a branch such as `task1/m2-analysis`, commit the relevant
files, and open a pull request. Coordinate one active notebook editor at a time
to keep notebook merges manageable.

## 7. Prepare and upload Task 2 photos

First read the [collection guide](data-collection.md), including the class
definitions and ten-photo shooting checklist. The configured classes are `mug`,
`paper_cup`, `plastic_bottle`, `aluminium_can`, and `drink_carton`.
Coordinate group IDs in the [shared object register](../data/task2/object-groups.md).
Member identifiers are `M1`, `M2`, and `M3`; use your assigned identifier below.

Keep camera originals outside the repository. For example:

```text
C:\Users\Alice\Pictures\COMP4930-photos\
  mug\
    m2_mug_01\
      session_01\
        IMG_1001.jpg
        IMG_1002.jpg
      session_02\
        IMG_1041.jpg
```

The required nesting is `class_name/object_group_id/session_id/photo`.
Use lowercase identifiers starting with a letter, followed by letters, digits
or underscores, up to 40 characters. Windows-reserved names such as `con` and
`nul` are rejected. Camera filenames may retain their original names. Export
HEIC/HEIF or Live Photo stills to JPEG or PNG before importing.

For M2's first batch:

```powershell
git switch main
git pull --ff-only
git switch -c photos/m2-batch1

mise exec -- python scripts/prepare_photos.py --member M2 --source "$HOME\Pictures\COMP4930-photos"
```

Before staging, open `data/task2/manifests/M2.csv` and fill `lighting`, `background`
and useful `notes`. Save it as UTF-8. Check the photos and update the shared object
register for any new designs. Leave `reviewer` empty until another member has
checked the photos and collection records. Then commit and upload:

```powershell
git status --short
git add -- data/task2/images/M2 data/task2/manifests/M2.csv data/task2/object-groups.md
git diff --cached --stat
git commit -m "data: add M2 task 2 photos"
git push -u origin photos/m2-batch1

gh pr create --base main --head photos/m2-batch1 --title "Add M2 Task 2 photos" --web
```

The preparation command corrects camera orientation, creates RGB JPEGs up to
1,024 pixels on the longest edge at quality 90, and records checksums. It keeps
originals intact. Its generated names include the object group, session and a
content-hash prefix.

**`git push` uploads the committed images and manifest to the public repository.**
The pull-request command opens the review form in your browser. Complete that
form. Another member checks the labels and collection records before merging.

| Output | M2 location |
| --- | --- |
| JPEG dataset copies | `data/task2/images/M2/<class_name>/` |
| Collection manifest | `data/task2/manifests/M2.csv` |

Preserve the manifest's identity and checksum columns. Additional annotation
columns are retained. Importing another batch merges new records; reimporting
unchanged photographs preserves existing records and annotations. Every member
owns their own manifest, and imports for that member should run one at a time.

The reviewer leaves feedback on the pull request. On the same photo branch,
pull any remote changes before editing:

```powershell
git switch photos/m2-batch1
git pull --ff-only
```

Apply the agreed corrections and leave `reviewer` empty for corrected image rows
until they have been checked again. Commit and push those changes to the existing
pull request:

```powershell
git add -A -- data/task2/images/M2 data/task2/manifests/M2.csv data/task2/object-groups.md
git diff --cached --stat
git commit -m "data: update M2 photo review"
git push
```

After the reviewer confirms the photos and records, fill their ID in `reviewer`
and commit/push the CSV update with the same commands. If the first review needs
no corrections, record their confirmed ID directly in that review update.
The reviewer checks the final changes before merging. For a label or group
correction, follow the [collection guide's correction steps](data-collection.md#8-review-prepare-and-upload)
so the image path and manifest stay consistent.

Use `photos/m2-batch2` for the next reviewed batch. Replace M2 with M1 or M3 as
appropriate. An import adding zero photos may still leave annotation or register
changes to commit; check `git status --short`.
The importer reports duplicate sources, conflicting labels or changed outputs
as errors. Review those records before retrying. If an import was interrupted,
retrying adopts matching JPEGs already written and completes the manifest.

Once a pull request is merged, everyone receives the shared dataset with:

```powershell
git switch main
git pull --ff-only
```

## Legion WSL2 GPU setup

Use the current NVIDIA **Windows** driver. Open administrator PowerShell:

```powershell
wsl --install -d Ubuntu
```

Restart Windows if prompted, open Ubuntu, and create its Linux username/password.
Run these commands in **Ubuntu**, keeping this clone in the Linux home directory:

```bash
sudo apt update
sudo apt install -y git curl gh
curl https://mise.run | sh
export PATH="$HOME/.local/bin:$PATH"
mkdir -p ~/Projects
cd ~/Projects
git clone https://github.com/PenSul/COMP4930SEF-Project.git Project
cd Project
mise trust
mise install
mise exec -- python -m pip install -r requirements-gpu.txt
nvidia-smi
mise exec -- python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

Add the mise installer directory to subsequent Ubuntu sessions with the same
`export PATH` command, or follow [mise shell setup](https://mise.jdx.dev/installing-mise.html#shells).
This Linux clone creates its own virtual environment. Configure Git identity and
run the two `gh auth` commands from step 2 inside Ubuntu before pushing results.

Proceed with GPU training when TensorFlow lists a GPU. Launch JupyterLab with
`mise run lab`; open the displayed local URL in your Windows browser if needed.
Use `requirements-dev.txt` as well if you want linting and tests on the Legion.
An unresolved GPU setup issue should be investigated in one bounded session,
then training can move to Colab while the setup issue is handled separately.

References: [TensorFlow installation](https://www.tensorflow.org/install/pip),
[NVIDIA CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html),
[Microsoft WSL installation](https://learn.microsoft.com/en-us/windows/wsl/install).

## Colab fallback

Clone the public repository into a Colab GPU runtime, install `requirements.txt`
into that runtime, and record its Python/package versions. Use the project directory
as the notebook's working directory. Colab supplies its own GPU drivers and CUDA
environment. Save checkpoints outside its temporary filesystem before ending the
session. The [Colab FAQ](https://research.google.com/colaboratory/faq.html) documents
resource limits; free GPU availability varies.
