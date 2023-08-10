import logging
import os
import subprocess
from pathlib import Path

from hera.workflows import Container, Parameter, Steps, Workflow
from hera.workflows.models import TTLStrategy

from argo_assistant import environment_management as aem

LOGGER = logging.getLogger()

DEFAULT_TTL = 90  # seconds
DEFAULT_ARGO_NODE_TYPE = "user"
DEFAULT_K8S_SELECTOR_LABEL = "eks.amazonaws.com/nodegroup"


class NebariWorkflow(Workflow):
    """Hera Workflow object with required/reasonable default for running
    on Nebari
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if "ttl_strategy" in kwargs.keys():
            self.ttl_strategy = kwargs["ttl_strategy"]
        else:
            self.ttl_strategy = TTLStrategy(
                seconds_after_completion=DEFAULT_TTL,
                seconds_after_success=DEFAULT_TTL,
                seconds_after_failure=DEFAULT_TTL,
            )

        if "node_selector" in kwargs.keys():
            self.node_selector = kwargs["node_selector"]
        else:
            self.node_selector = {DEFAULT_K8S_SELECTOR_LABEL: DEFAULT_ARGO_NODE_TYPE}

        self.namespace = os.environ["ARGO_NAMESPACE"]

        self.labels = aem.get_labels()


def create_conda_command(
    script_path,
    conda_env,
    stdout_path="stdout.txt",
):
    """Workflows need to be submitted via a bash command that runs a
    python script. This function creates a conda run command that
    will run a script from a given location using a given conda
    environment.

    Parameters
    ----------
    script_path: str
        Path to the python script (including extension) to be run on Argo
    conda_env: str
        Conda environment name in which to the run the `script_path`
    stdout_path: str
        Local Nebari path (for your user) for standard output from
        the given script. Defaults to `stdout.txt`.

    Returns
    -------
    String bash command
    """

    conda_command = f'conda run -n {conda_env} python "{script_path}" >> {stdout_path}'
    return conda_command


def create_bash_container(name="bash-container"):
    """Create a workflow container that is able to recieve bash commands"""
    bash_container = Container(
        name="bash-container",
        image="thiswilloverridden",
        inputs=[
            Parameter(name="bash_command")
        ],  # inform argo that an input called bash_command is coming
        command=["bash", "-c"],
        args=["{{inputs.parameters.bash_command}}"],  # use the input parameter
    )
    return bash_container


def submit_argo_script(script_path, conda_env, stdout_path="stdout.txt"):
    """Submit a script to be run via Argo in a specific environment"""
    validated = validate_submission(script_path, conda_env)

    if not validated:
        raise RuntimeError("Unable to submit Argo workflow")

    conda_command = create_conda_command(script_path, conda_env, stdout_path)

    LOGGER.debug("Submitting command {conda_command} to Argo")

    with NebariWorkflow(
        generate_name="workflow-name-",
        entrypoint="steps",
    ) as w:
        bash_container = create_bash_container()
        with Steps(
            name="steps",  # must match Workflow entrypoint
            annotations={"go": "here"},
        ):
            bash_container(
                name="step-name",
                arguments=[Parameter(name="bash_command", value=conda_command)],
            )

    workflow = w.create()
    return workflow


def validate_submission(script_path, conda_env):
    """Validates and error checks for common issues.
    TODO: this is temporary until we get better logging for Argo
    """
    success = True
    # ensure that the script exists
    script_path = Path(script_path)
    if not script_path.exists():
        success = False
        LOGGER.error(f"Script file does not exist at {script_path}")

    # ensure that the conda env exists (loose check)
    result = subprocess.run(
        ["conda env list"],
        shell=True,
        capture_output=True,
        text=True,
    )
    if conda_env not in result.stdout:
        success = False
        LOGGER.error(f"Conda env {conda_env} does not exist")

    return success
