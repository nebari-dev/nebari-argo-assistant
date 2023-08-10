from pathlib import Path

import pytest
from s3fs import S3FileSystem

from argo_assistant.io import get_file, put_file, remove_file, s3


@pytest.fixture(scope="session")
def temp_local_file(tmp_path_factory):
    """Temporary local file for testing"""
    path = tmp_path_factory.mktemp("data") / "local_file.py"

    with open(path, "w") as f:
        f.write(
            "This is test file. It should have been auto-removed. \
            If found, please remove."
        )

    return path


@pytest.fixture(scope="session")
@pytest.mark.nebari_resources
def temp_s3_file(temp_local_file, s3_bucket):
    """Temporary remote file on s3 for testing"""
    s3()
    remote_path = f"{s3_bucket}/deleteme_testfile.py"
    put_file(temp_local_file, remote_path)

    yield remote_path

    # remove remote copy
    remove_file(remote_path)


def test_s3_client():
    client = s3(key=None, secret=None, region=None)

    assert isinstance(client, S3FileSystem)


@pytest.mark.nebari_resources
def test_get_file(temp_s3_file):
    local_path = "temp_local_test.py"
    get_file(temp_s3_file, local_path)
    local_path = Path(local_path)
    assert local_path.exists()

    # remove local copy
    local_path.unlink()


@pytest.mark.nebari_resources
def test_put_remove_file(temp_local_file, s3_bucket):
    remote_path = f"{s3_bucket}/temp_file_test.py"

    client = put_file(temp_local_file, remote_path)
    assert client.exists(remote_path)

    remove_file(remote_path)
    assert not client.exists(remote_path)
