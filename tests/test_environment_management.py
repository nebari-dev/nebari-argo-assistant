from argo_assistant import environment_management as aem


def test_setup_argo_environment_verbose_true():
    # setup argo and hera environment variables
    aem.setup_argo_environment(verbose=True)


def test_setup_argo_environment_verbose_false():
    # setup argo and hera environment variables
    aem.setup_argo_environment(verbose=False)
