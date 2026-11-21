# Run the Task 1 comparison on the Legion

Run the notebook in **WSL2 Ubuntu** using the Linux clone and its own Python environment. For a new machine, install the NVIDIA driver in Windows and follow the [project's WSL2 setup](team-setup.md#legion-wsl2-gpu-setup). In Windows PowerShell, `wsl -l -v` should show version 2 for Ubuntu. [Microsoft WSL installation](https://learn.microsoft.com/en-us/windows/wsl/install) · [NVIDIA CUDA on WSL](https://docs.nvidia.com/cuda/wsl-user-guide/index.html)

## Verify the GPU

From a clean checkout in **Ubuntu Bash**, update the code, install the pinned GPU dependencies, and start a results branch.

```bash
cd ~/Projects/Project
git switch main
git pull --ff-only
git switch -c task1/legion-results
mise trust
mise install
mise exec -- python -m pip install -r requirements-gpu.txt
mise exec -- python -m pip check
nvidia-smi
```

Check that TensorFlow can actually execute a matrix multiplication on the GPU. The output should identify `GPU:0` and the value `32.0`. Run this check from the same Ubuntu terminal you will use to launch JupyterLab. [TensorFlow GPU guide](https://www.tensorflow.org/guide/gpu)

```bash
mise exec -- python - <<'PY'
import tensorflow as tf

gpus = tf.config.list_physical_devices("GPU")
if not gpus:
    raise SystemExit("TensorFlow cannot see a GPU in this Ubuntu environment.")
tf.config.experimental.set_memory_growth(gpus[0], True)
tf.config.set_soft_device_placement(False)
with tf.device("/GPU:0"):
    x = tf.ones((32, 32))
    product = tf.linalg.matmul(x, x)
print(product.device, float(product[0, 0].numpy()))
PY
```

If TensorFlow cannot find the GPU, compare `nvidia-smi` in Windows and Ubuntu to locate the problem. If both show the GPU, check that `mise exec -- python -m pip show tensorflow` points inside this clone's `.venv` and follow the WSL2 verification instructions in the [TensorFlow pip installation guide](https://www.tensorflow.org/install/pip).

## Run the notebook

Choose one command at a time in Ubuntu. Open the URL JupyterLab prints, open `project_report.ipynb`, select the project's Python kernel and use **Kernel → Restart Kernel and Run All Cells**. Check the Task 1 output for the chosen mode and device. Save the notebook after the cells finish. When switching modes, stop JupyterLab using Ctrl+C in its terminal, confirm shutdown, and launch it again with the next command. Each new kernel inherits the mode from its server.

| Stage | Launch command | What to check |
| --- | --- | --- |
| Preview | `mise run lab` | Read the methods and run the definitions. This is the default mode. |
| Smoke | `TASK1_MODE=smoke mise run lab` | Exercise all three candidates on a small sample of real CIFAR data. Check fitting, validation and checkpoint reloading. The first run needs internet for the dataset and pretrained weights. |
| Train | `TASK1_MODE=train mise run lab` | Fit the three candidates on the same split for seeds 42, 43 and 44. Review the nine validation results, training curves, runtime and class errors. |
| Final | `TASK1_MODE=final mise run lab` | After reviewing the completed comparison, evaluate the selected model's seed-42 checkpoint on the official test set and save the report. |

The full comparison uses 20,000 training and 5,000 validation images. Mean validation accuracy across the three seeds selects the model, with mean macro-F1 and then parameter count resolving ties. The 5,000 official test images provide the final estimate. Use the same batch size and experiment settings for **train** and **final**.

Plug the Legion into power and keep it awake throughout training. If a session stops, relaunch **train** with the same code, batch size and artifacts directory. Completed candidate/seed runs can be reused. An interrupted candidate/seed run starts again. If GPU memory runs out at the default batch size of 32, close other GPU workloads or select a batch size of 16. A changed batch size creates a separate experiment. Use the smaller batch size consistently for all nine runs and the final step.

```bash
TASK1_BATCH_SIZE=16 TASK1_MODE=train mise run lab
# After reviewing the nine runs, stop the server and launch the final evaluation.
TASK1_BATCH_SIZE=16 TASK1_MODE=final mise run lab
```

Run one Task 1 kernel at a time against this checkout. Keep the completed notebook outputs for the report. Back up `artifacts/task1/` with its directory structure. After final evaluation, `artifacts/task1/final/selection.json` identifies the winning `.keras` checkpoint, its SHA-256, the input format, the label order and the `representation` layer for Task 2. The checkpoints and download caches stay local. Share the saved notebook through the [team PR workflow](development-workflow.md).
