# nebari-argo-assistant
A suite of tools to make submitting Argo workflows on Nebari easier

## Usage

### Setting up the run script

To use the Argo Assistant, first you will create the script that you want
to run in Argo. There is an example script provided
[basic_conda_usage-RUN.py](https://github.com/nebari-dev/nebari-argo-assistant/blob/main/examples/basic_conda_usage-RUN.py) 
that you can use for testing. 

### Launching the workflow

You will launch this script by submitting it to the Argo scheduler. The example workflow below is also stored in 
[basic_conda_usage-LAUNCH.py](https://github.com/nebari-dev/nebari-argo-assistant/blob/main/examples/basic_conda_usage-LAUNCH.py).

First, you will need to setup the argo environment. Behind the scenes, this will setup 
some necessary environment variables for using Argo and Hera. 

```python
from pathlib import Path

from argo_assistant import environment_management as aem
from argo_assistant.workflows import submit_argo_script

# setup argo and hera environment variables
aem.setup_argo_environment(verbose=False)
```

Next you will submit the script which you want to run (e.g. `basic_conda_usage-RUN.py` above) to Argo. 

You will also need to define the conda environment in which you want to run the script and the output path. 

```python
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
```
Finally, you can check the status via the Argo Assistant API or you can visit the UI:

```python
# check status programmatically or visit the UI
status = workflow.status
```

## Installation

To install the package:

```python
pip install -e .
```

Alternatively, there is a developer install, `dev`, and a testing install, `test`.

```python
pip install -e .['dev']
```
