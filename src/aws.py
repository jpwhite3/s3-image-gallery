import boto3
import logging
from botocore.errorfactory import ClientError

LOG = logging.getLogger(__name__)
S3_CLIENT = boto3.client("s3")
S3_RESOURCE = boto3.resource("s3")


def list_objects_generator(bucket, prefix=None, paginator="list_objects_v2"):
    param_dict = {"Bucket": bucket}
    if prefix:
        param_dict["Prefix"] = prefix
    response_iterator = S3_CLIENT.get_paginator(paginator).paginate(**param_dict)
    for response in response_iterator:
        yield response


def delete_prefix_from_s3(bucket, prefix, delete_versions=False):
    paginator = "list_object_versions" if delete_versions else "list_objects_v2"
    for page in list_objects_generator(bucket, prefix=prefix, paginator=paginator):
        for file in page.get("Contents", []):
            LOG.debug("deleting s3://%s/%s", bucket, file["Key"])
            S3_CLIENT.delete_object(Bucket=bucket, Key=file["Key"])


def upload_to_s3(source_file, bucket, destination_key):
    LOG.debug("uploaded %s to s3://%s/%s", source_file, bucket, destination_key)
    S3_RESOURCE.meta.client.upload_file(source_file, bucket, destination_key)


def s3_key_exists(bucket, key):
    try:
        S3_CLIENT.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as err:
        if "404" in str(err):
            return False
        raise
