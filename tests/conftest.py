# A place for pytest fixtures and configuration
import pytest

S3_BUCKET = "jatic-data"


@pytest.fixture(scope="session")
def s3_bucket():
    """s3 bucket used for testing. Files should not be left in
    the bucket after testing!
    """
    return S3_BUCKET
