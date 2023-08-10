"""Input/Output operations

For IO operations on AWS GovCloud S3, the recommended approach to
environment variables for this module is to setup a `.env` file
with the following entries:

```
AWS_ACCESS_KEY_ID='your_access_key'
AWS_SECRET_ACCESS_KEY='your_secret_key'
AWS_DEFAULT_REGION='us-gov-west-1'
```

For IO operations on AWS GovCloud S3, set up an aws credentials file with
your access keys at `~/.aws/credentials`. The region `us-gov-west-1` is
required. The format is:

```
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
aws_default_region=us-gov-west-1
```

"""

import logging
import os
from pathlib import Path

import s3fs

LOGGER = logging.getLogger()


def boto_client(key=None, secret=None, region=None):
    """Create boto3 S3 client"""
    import boto3

    if not key:
        key = os.environ.get("AWS_ACCESS_KEY_ID", "UNSET")
        LOGGER.debug("setting AWS access key via env var")

    if not secret:
        secret = os.environ.get("AWS_SECRET_ACCESS_KEY", "UNSET")
        LOGGER.debug("setting AWS secret via env var")

    if not region:
        region = os.environ.get("AWS_DEFAULT_REGION", "UNSET")
        LOGGER.debug("setting AWS region via env var")

    client = boto3.client(
        "s3", aws_access_key_id=key, aws_secret_access_key=secret, region_name=region
    )

    return client


def s3(key=None, secret=None, region=None):
    """Create s3fs client"""

    if not key:
        key = os.environ.get("AWS_ACCESS_KEY_ID", "UNSET")
        LOGGER.debug("setting AWS access key via env var")

    if not secret:
        secret = os.environ.get("AWS_SECRET_ACCESS_KEY", "UNSET")
        LOGGER.debug("setting AWS secret via env var")

    if not region:
        region = os.environ.get("AWS_DEFAULT_REGION", "UNSET")
        LOGGER.debug("setting AWS region via env var")

    client = s3fs.S3FileSystem(
        key=key, secret=secret, config_kwargs={"region_name": region}
    )

    return client


def get_file(remote_path, local_path=None, client=None):
    """Download a file from s3"""
    if not client:
        client = s3()

    # if local path not provided, use the remote filename
    if not local_path:
        local_path = Path(remote_path).name

    client.get(remote_path, local_path)

    return client


def put_file(local_path, remote_path=None, client=None):
    """Upload a file to s3"""
    if not client:
        client = s3()

    # if local path not provided, use the remote filename
    if not remote_path:
        remote_path = Path(local_path).name

    client.put(str(local_path), str(remote_path), recursive=True)

    return client


def remove_file(remote_path, client=None):
    if not client:
        client = s3()

    client.rm_file(remote_path, recursive=True)
