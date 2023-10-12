import boto3
import os
from glob import glob
import json
import re
import datetime

import streamlit as st

BUCKET = os.environ.get("BUCKET")
USE_LOCAL = os.environ.get("USE_LOCAL", "FALSE").lower() == "true" 
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


def fetch_local(ta):
    files = glob("report*.json", root_dir=f"outputs/{ta}")
    return {
        file: json.load(open(f"outputs/{ta}/{file}"))
        for file in files
    }


def download(ta):
    objects = s3.list_objects(Bucket=BUCKET, Prefix=ta)
    handles = [content["Key"] for content in objects['Contents']]
    files = {handle: s3.get_object(Bucket=BUCKET, Key=handle) for handle in handles}
    return {key: json.load(body["Body"]) for key,body in files.items()}


def generate_timestamp_to_filenames(ta):
    return {format_timestamp_from_filename(f): f for f in download(ta)}


def select_report(ta):
    if not USE_LOCAL:
        report_files = download(ta)
    else:
        report_files = fetch_local(ta)
    if len(report_files) == 0:
        st.warning("No reports available")
        st.stop()
    timestamp_to_filename = {format_timestamp_from_filename(f): f for f in report_files}
    selected_timestamp = st.selectbox("Select a report", sorted(timestamp_to_filename.keys(), reverse=True))
    return report_files[timestamp_to_filename[selected_timestamp]]