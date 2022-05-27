import boto3

S3_CLIENT = boto3.client("s3")
S3 = boto3.resource("s3")
BUCKET = "jpw3-secure-backup"


def list_objects(bucket, prefix=None, paginator="list_objects_v2") -> dict:
    param_dict = {"Bucket": bucket}
    if prefix:
        param_dict["Prefix"] = prefix
    response_iterator = S3_CLIENT.get_paginator(paginator).paginate(**param_dict)
    for response in response_iterator:
        yield response


def set_storage_class(key: str, storage_class: str = "INTELLIGENT_TIERING") -> None:
    copy_source = {"Bucket": BUCKET, "Key": key}
    S3.meta.client.copy(
        copy_source,
        BUCKET,
        copy_source["Key"],
        ExtraArgs={"StorageClass": storage_class, "MetadataDirective": "COPY"},
    )


def main() -> None:
    for response in list_objects(BUCKET):
        for record in response["Contents"]:
            if record["StorageClass"] != "INTELLIGENT_TIERING":
                print(record["Key"])
                set_storage_class(record["Key"])


if __name__ == "__main__":
    main()
