# COMP 4930SEF Project

TensorFlow/Keras coursework covering image classification, a team-collected
photo dataset, and AG News topic classification.

The repository currently contains the development environment, report outline,
photo importer, and collection instructions. Model experiments are the next stage.

## Get started

Install [Git](https://git-scm.com/install/),
[mise](https://mise.jdx.dev/installing-mise.html), and
[GitHub CLI](https://cli.github.com/). Then run:

```sh
git clone https://github.com/PenSul/COMP4930SEF-Project.git Project
cd Project
mise trust
mise install
mise exec -- python -m pip install -r requirements-dev.txt
mise run lab
```

Open `project_report.ipynb`. Mise supplies Python 3.12.15 and a local `.venv`.
The same commands work in Windows PowerShell and Linux shells.

- **First Windows setup, Git login and uploads:** [Team setup](docs/team-setup.md)
- **Legion GPU training:** [WSL2 setup](docs/team-setup.md#legion-wsl2-gpu-setup)
- **Photo classes, capture rules and labels:** [Collection guide](docs/data-collection.md)
- **Experiments and submission milestones:** [Project plan](docs/project-plan.md)

## Development

```sh
mise run test
mise run lint
mise run typecheck
```

The checks run on Windows and Linux in GitHub Actions. Keep simple functions
typed and document non-obvious decisions. Coordinate edits to the report notebook;
use member branches and pull requests for contributions.

## Data and outputs

Task 2's standardised JPEGs belong in `data/task2/images/M1/`, `M2/`, or `M3/`.
Each member has a CSV in `data/task2/manifests/`. The importer creates these
folders. Agree on the five classes and fill `data/task2/classes.json` before
importing photos; it is intentionally empty at this stage.

Keep originals outside the repository. Downloaded datasets, caches, model
checkpoints under `artifacts/`, and the two supplied reference PDFs are ignored.
Keep report outputs and small experiment summaries in Git. TensorFlow/Keras and
Matplotlib caches are local to `.cache/`.

The submission consists of the executed notebook, the required declaration and
contribution document, and a 5–8 minute team video. The deadline is
4 December 2026, 23:59 Hong Kong time; our target is 3 December.
