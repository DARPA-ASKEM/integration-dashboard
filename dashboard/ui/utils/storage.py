import boto3
import os
from glob import glob
import json

BUCKET = os.environ.get("BUCKET")
s3 = boto3.client("s3")

def download(ta="ta1"):
    objects = s3.list_objects(Bucket=BUCKET, Prefix=ta)
    handles = [content["Key"] for content in objects['Contents']]
    files = {handle: s3.get_object(Bucket=BUCKET, Key=handle) for handle in handles}
    return {key: json.load(body["Body"]) for key,body in files.items()}


