import json
import datetime
import os
import re
from functools import reduce
from collections import defaultdict

import streamlit as st
import pandas as pd

from dashboard.generate.storage import download


def custom_title(s):
    # List of words you want to fully capitalize
    FULL_CAPS = ['pdf', 'amr']

    words = s.replace('_', ' ').split()
    capitalized_words = [word.upper() if word in FULL_CAPS else word.title() for word in words]
    return ' '.join(capitalized_words)

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

report_files = download()
timestamp_to_filename = {format_timestamp_from_filename(f): f for f in report_files}

# Let the user select a report based on formatted timestamps
st.title("TA1 Integration Dashboard")
selected_timestamp = st.selectbox("Select a report", sorted(timestamp_to_filename.keys(), reverse=True))

report = report_files[timestamp_to_filename[selected_timestamp]]

test_results = defaultdict(lambda: defaultdict())

for scenario, content in report.items():
    for operation, tests in content["operations"].items():
        for name, result in tests.items():
            test_results[name][(content["name"], operation)] = result

scenarios = [report[scenario]["name"] for scenario in report.keys()]
operations = list(reduce(lambda left, right: left.union(right), [set(content["operations"].keys()) for content in report.values()], set()))
tests = sorted([i for i in test_results.keys() if i != "Logs"], reverse=True)
tests.append("Logs")


dataframes = {name: pd.DataFrame(index=scenarios, columns=operations) for name in tests}

st.sidebar.markdown("""
# TA1

TA1 integration status and quality metrics.
    
The current metrics are:
- Status of `knowledge-middleware` integration
- F-score for conversion of code/equations to AMR
- Execution time
- Application logs
""")
st.write("### Scenario Overview")
scenarios_overview = ""
for kk, vv in sorted(report.items(), key=lambda item: item[1]['name']):
    scenarios_overview += f"- **{vv['name']}**: {vv['description']}\n"
st.write(scenarios_overview)

for test in tests:
    df = dataframes[test]
    results = test_results[test]
    for (scenario_name, operation), result in results.items():
        df.at[scenario_name, operation] = result
    st.write(f"### {test}")
    df.replace({False: "❌", True: "✅", None: ""}, inplace=True)
    df.columns = [custom_title(col) for col in df.columns]
    df = df.sort_index()
    df