import pytest

from argo_assistant import environment_management as aem


@pytest.mark.nebari_resources
def test_setup_argo_environment_verbose_true():
    # setup argo and hera environment variables
    aem.setup_argo_environment(verbose=True)


@pytest.mark.nebari_resources
def test_setup_argo_environment_verbose_false():
    # setup argo and hera environment variables
    aem.setup_argo_environment(verbose=False)
