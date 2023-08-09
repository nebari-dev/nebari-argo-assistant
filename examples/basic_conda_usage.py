"""
This workflow submits a script to be run on a specific conda environment
via Argo.
"""


from argo_assistant import environment_management as aem
from argo_assistant.workflows import submit_argo_script

# setup argo and hera environment variables
aem.setup_argo_environment(verbose=False)


script_path = "/home/kcpevey@quansight.com/argo.py"
conda_env = "kcpevey@quansight.com-argo_v1"
workflow = submit_argo_script(script_path=script_path, conda_env=conda_env)

status = workflow.status
