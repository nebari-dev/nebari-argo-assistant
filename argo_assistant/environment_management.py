import os
import re

from hera.shared import global_config
from rich import print


def setup_argo_environment(verbose=True):
    """Setup the environment variables and global config settings
    required for running Argo.

    >>> setup_argo_environment()
    >>> setup_argo_environment(verbose=False)

    Parameters
    ----------
    verbose: bool
        If True, pretty prints all Argo related env vars (with secrets
        partially redacted). No return if False.

    Returns
    -------
    Print display of environment variables if `verbose=True`
    """

    # global config set via env vars doens't work properly
    global_config_host = f"https://{os.environ['ARGO_SERVER'].rsplit(':')[0]}{os.environ['ARGO_BASE_HREF']}/"
    global_config.host = global_config_host
    global_config.token = os.environ['ARGO_TOKEN'] 
    
    if verbose:
        display_argo_env_vars()


def display_argo_env_vars():
    """Display the argo and hera environment variables in an easily readable format.
    Secrets are partially redacted to allow comparison but not leakage.
    """
    argo_token = os.environ.get("ARGO_TOKEN", "UNSET")
    if argo_token == "UNSET":
        argo_display = argo_token
    else:
        argo_display = f"{argo_token[:5]}...{argo_token[-5:]}"

    hera_token = os.environ.get("HERA_TOKEN", "UNSET")
    if hera_token == "UNSET":
        hera_display = hera_token
    else:
        hera_display = f"{hera_token[:5]}...{hera_token[-5:]}"

    display = f"""
    ***Argo environment variables:***
    ARGO_SERVER={os.environ.get('ARGO_SERVER', 'UNSET')}
    ARGO_HTTP1={os.environ.get('ARGO_HTTP1', 'UNSET')}
    ARGO_SECURE={os.environ.get('ARGO_SECURE', 'UNSET')}
    ARGO_BASE_HREF={os.environ.get('ARGO_BASE_HREF', 'UNSET')}
    ARGO_TOKEN={argo_display}
    ARGO_NAMESPACE={os.environ.get('ARGO_NAMESPACE', 'UNSET')}
    KUBECONFIG={os.environ.get('KUBECONFIG', 'UNSET')}

    ***Hera environment variables:***
    GLOBAL_CONFIG_HOST={os.environ.get('GLOBAL_CONFIG_HOST', 'UNSET')}
    GLOBAL_CONFIG_NAMESPACE={os.environ.get('GLOBAL_CONFIG_NAMESPACE', 'UNSET')}
    HERA_TOKEN={hera_display}

    ***Argo REST api endpoint:***
    {os.environ.get('GLOBAL_CONFIG_HOST', 'UNSET')}api/v1/
    """

    print(display)


def sanitize_label(label: str) -> str:
    """
    The sanitize_label function converts all characters that are not
    alphanumeric or a - to their hexadecimal ASCII equivalent. This is
    because kubernetes will complain if certain characters are being
    used. This is the same approach taken by Jupyter for sanitizing.

    On the Nebari Workflow Controller, there is a `desanitize_label`
    function that reverses these changes so we can then perform a user
    look up.

    >>> sanitize_label("user@email.com")
    user-40email-2ecom

    Parameters
    ----------
    label: str
        Username to be sanitized (typically Jupyterhub username)

    Returns
    -------
    Hexadecimall ASCII equivalent of `label`

    """
    label = label.lower()
    pattern = r"[^A-Za-z0-9]"
    return re.sub(pattern, lambda x: "-" + hex(ord(x.group()))[2:], label)


def get_labels():
    """Get labels required for Argo workflow. Nebari uses a shared Argo
    token by default instead of individual user tokens. Therefore we need
    to explicitly set the user for each Hera Workflow.

    Returns
    -------
    dict of labels for Hera Workflow objects
    """
    username = os.environ["JUPYTERHUB_USER"]
    labels = {
        "workflows.argoproj.io/creator-preferred-username": sanitize_label(username),
        'jupyterflow-override': 'true',
    }
    return labels
