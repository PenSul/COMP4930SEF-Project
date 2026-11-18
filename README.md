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
folders. The agreed classes are `mug`, `paper_cup`, `plastic_bottle`,
`aluminium_can`, and `drink_carton`, configured in `data/task2/classes.json`.
Aim for 200 usable photos per member, covering every class. Follow the
[shooting checklist](docs/data-collection.md#6-ten-useful-photographs-of-each-object)
and coordinate objects in the [shared register](data/task2/object-groups.md).

Keep originals outside the repository. Downloaded datasets, caches, model
checkpoints under `artifacts/`, and the two supplied reference PDFs are ignored.
Keep report outputs and small experiment summaries in Git. TensorFlow/Keras and
Matplotlib caches are local to `.cache/`.
