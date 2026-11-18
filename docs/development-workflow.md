# Daily development and pull requests

Use this after completing [team setup](team-setup.md). Run commands in PowerShell
from your local `Project` directory. The same Git commands work in WSL2.

**Work on your own branch, push it, and open a pull request (PR). PenSul reviews
and merges it into `main`.** We follow this by team agreement; GitHub branch
protection has not been enabled. Keep PRs small enough to review one idea at a time.

| Action | What it does |
| --- | --- |
| `git commit` | Saves a local snapshot on your current branch |
| `git push` | Uploads committed snapshots to that branch on GitHub |
| Open a PR | Asks the team to review a proposed change to `main` |
| Merge the PR | Adds the reviewed change to `main` |
| `git pull --ff-only` | Downloads updates to your current branch without creating a merge commit |

## 1. Before starting a new task

Check for unfinished work first:

```powershell
git status --short --branch
```

If files are modified, save and commit them on their existing task branch before
switching tasks. An unfinished contribution can stay on a branch with a draft PR.
When the working tree is clean:

```powershell
git switch main
git pull --ff-only
mise exec -- python -m pip install -r requirements-dev.txt
git switch -c task3/m3-data
mise run lab
```

`task3/m3-data` is an example: replace the member and topic with your assignment.
Other examples are `task1/m2-training` and `photos/m2-batch1`. Create a new branch
for each separate contribution; `git switch -c` is used only when creating it.

Agree who is editing `project_report.ipynb` before starting. One person edits or
executes the shared notebook at a time. Keep changes inside your agreed task
sections, preserve teammates' cells and outputs, and merge small increments.
The Task 3 owner starts with the [Task 3 guide](task3-guide.md).

## 2. Continuing an existing branch

With your work saved and committed:

```powershell
git switch task3/m3-data
git pull --ff-only
git fetch origin
git merge origin/main
```

The first pull updates your contribution branch after its first push. Skip it
if the branch has never been pushed and has no upstream yet. The final two
commands bring the latest shared work into your branch. Reinstall dependencies
if requirements changed.

If Git reports conflicts, pause editing and coordinate with the other author.
For a notebook conflict, agree which cells to preserve before resolving it.
`git merge --abort` returns to the state before an unfinished merge. Keep the
working tree clean before starting a merge so that this recovery is straightforward.
If `git pull --ff-only` refuses because histories diverged, send the error to
PenSul; keep your branch and local commits intact.

## 3. After finishing a useful piece of work

Save the notebook and run the project checks:

```powershell
mise run test
mise run lint
mise run typecheck
```

For model changes, also run the relevant notebook cells on a small batch and
record the result. Current automated tests cover photo preparation; they do
not establish model quality. Full training belongs on the Legion or an agreed
GPU runtime. Preserve useful report outputs and remove accidental debug output.

Review and stage the files you intend to contribute. This example stages the
report; name any additional files explicitly:

```powershell
git status --short
git diff --stat
git diff -- project_report.ipynb
git add -- project_report.ipynb
git diff --cached --stat
git diff --cached
git commit -m "feat: prepare AG News data and validation split"
git push -u origin task3/m3-data
```

The staged diff is the content of the commit. Keep downloaded news data, original
photos, `.venv`, credentials and checkpoints out of it. Small metric summaries,
figures and notebook outputs belong in the report. Use
[the photo upload commands](team-setup.md#7-prepare-and-upload-task-2-photos)
for Task 2 JPEGs and manifests.

## 4. Open a PR and request review

```powershell
gh pr create --base main --head task3/m3-data --web
```

Complete the browser form using the PR template and select **PenSul** in its
**Reviewers** control. Explain what changed, why the method fits the task, which
sources informed it, and what you actually checked. For unfinished work, choose
**Create draft pull request** from the browser's create-button dropdown and list
what remains. Request PenSul's review when the draft is ready for review.
The command opens this form; [gh pr create](https://cli.github.com/manual/gh_pr_create)
documents the browser workflow.

Share the PR link with PenSul. PenSul can bring that link into this project chat
for code inspection, methodology research and discussion before approving it.
Allow time for that review before a large training run or final test evaluation.

The owner checks the implementation and evidence, confirms the scope follows the
brief, and checks both **Python 3.12 / ubuntu-latest** and
**Python 3.12 / windows-latest** in the PR. CI checks installation, the dataset
builder, helper tests, lint, types and notebook structure. Model performance and
data leakage also need review of the actual notebook and experiment outputs.

## 5. Apply review feedback on the same branch

```powershell
git switch task3/m3-data
git pull --ff-only
```

Make the agreed changes, save and rerun the affected checks. Then:

```powershell
git add -- project_report.ipynb
git diff --cached
git commit -m "fix: address AG News split review"
git push
```

The existing PR updates automatically. Reply to the review with the change and
its evidence, then ask for another look. Use ordinary pushes; coordinate any
history repair with PenSul. Keep the PR open until the owner has reviewed its
latest version and discussions are resolved.

## 6. After the owner merges

PenSul uses **Create a merge commit** for the normal team workflow. This retains
the branch's commits and makes ordinary local branch deletion straightforward.
Everyone then downloads the accepted work:

```powershell
git switch main
git pull --ff-only
mise exec -- python -m pip install -r requirements-dev.txt
```

The contributor may remove their merged local branch:

```powershell
git branch -d task3/m3-data
```

If deletion is refused, keep the branch and ask PenSul to check it; a squash merge
or an extra local commit can cause this. Start the next task on a new branch from
the updated `main`.
