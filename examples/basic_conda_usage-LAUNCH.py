"""
This script submits a script to be run on a specific conda environment
via Argo.
"""

from pathlib import Path

from argo_assistant import environment_management as aem
from argo_assistant.workflows import submit_argo_script

# setup argo and hera environment variables
aem.setup_argo_environment(verbose=False)

# path to the script you're submitting to Argo
script_path = Path(__file__).parent.joinpath("basic_conda_usage-RUN.py")
# conda environment to run in
conda_env = "nebari-git-dask"
# output path will be relative to your home directory
stdout_path = "basic_conda_usage.out"

# submit the workflow
workflow = submit_argo_script(
    script_path=script_path,
    conda_env=conda_env,
    stdout_path=stdout_path,
)

# check status programmatically or visit the UI
status = workflow.status
