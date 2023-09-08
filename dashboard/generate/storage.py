import boto3
import os
from glob import glob
import json

BUCKET = os.environ.get("BUCKET")
s3 = boto3.client("s3")

def upload_reports(output_dir="services/knowledge-middleware/tests/output/", ta="ta1"):
    for handle in glob("report*.json", root_dir=output_dir):
        full_handle = os.path.join(ta, handle)
        local_handle = os.path.join(output_dir, handle)
        s3.upload_file(local_handle, BUCKET, full_handle)


def download(ta="ta1"):
    objects = s3.list_objects(Bucket=BUCKET, Prefix=ta)
    handles = [content["Key"] for content in objects['Contents']]
    files = {handle: s3.get_object(Bucket=BUCKET, Key=handle) for handle in handles}
    return {key: json.load(body["Body"]) for key,body in files.items()}


