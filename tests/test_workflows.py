import os

import pytest
from hera.workflows import Steps, script

from argo_assistant import environment_management as aem
from argo_assistant.workflows import NebariWorkflow


@script()
def echo(message: str):
    print(message)


@pytest.mark.nebari_resources
def test_NebariWorkflow_basic():
    """test basic construction of NebariWorkflow object and hello world example"""
    aem.setup_argo_environment(verbose=False)

    with NebariWorkflow(
        generate_name="hello-user",
        entrypoint="steps",
    ) as w:
        with Steps(name="steps"):
            echo(arguments={"message": "hello world"})

    w.create()
