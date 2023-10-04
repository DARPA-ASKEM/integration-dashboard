import boto3
import os
from glob import glob
import json
import re
import datetime

import streamlit as st

BUCKET = os.environ.get("BUCKET")
s3 = boto3.client("s3")


def format_timestamp_from_filename(filename):
    # Extract timestamp from filename
    match = re.search(r'report_(\d{8})_(\d{6})\.json', filename)
    if match:
        date_part, time_part = match.groups()
        # Convert to datetime object
        dt = datetime.datetime.strptime(f"{date_part}{time_part}", '%Y%m%d%H%M%S')
        # Return formatted string
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise Exception("Extra file was included")


def download(ta):
    objects = s3.list_objects(Bucket=BUCKET, Prefix=ta)
    handles = [content["Key"] for content in objects['Contents']]
    files = {handle: s3.get_object(Bucket=BUCKET, Key=handle) for handle in handles}
    return {key: json.load(body["Body"]) for key,body in files.items()}


def generate_timestamp_to_filenames(ta):
    return {format_timestamp_from_filename(f): f for f in download(ta)}


def select_report(ta):
    report_files = download(ta)
    timestamp_to_filename = {format_timestamp_from_filename(f): f for f in report_files}
    selected_timestamp = st.selectbox("Select a report", sorted(timestamp_to_filename.keys(), reverse=True))
    return report_files[timestamp_to_filename[selected_timestamp]]