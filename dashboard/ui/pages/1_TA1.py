import json
import datetime
import os
import re
from functools import reduce
from collections import defaultdict

import streamlit as st
import pandas as pd

from dashboard.ui.utils.storage import download


def custom_title(s):
    # List of words you want to fully capitalize
    FULL_CAPS = ['pdf', 'amr']

    words = s.replace('_', ' ').split()
    capitalized_words = [word.upper() if word in FULL_CAPS else word.title() for word in words]
    return ' '.join(capitalized_words)

def format_timestamp_from_filename(filename):
    # Extract timestamp from filename
    match = re.search(r'report(?:_local)?_(\d{8})_(\d{6})\.json', filename)
    if match:
        date_part, time_part = match.groups()
        is_local = "_local" if "_local" in filename else ""
        # Convert to datetime object
        dt = datetime.datetime.strptime(f"{date_part}{time_part}", '%Y%m%d%H%M%S')
        # Return formatted string
        return f'{dt.strftime("%Y-%m-%d %H:%M:%S")}{is_local}'
    else:
        raise Exception("Extra file was included")

report_files = download()
timestamp_to_filename = {format_timestamp_from_filename(f): f for f in report_files}

# Let the user select a report based on formatted timestamps
st.title("TA1 Integration Dashboard")
selected_timestamp = st.selectbox("Select a report", sorted(timestamp_to_filename.keys(), reverse=True))

report = report_files[timestamp_to_filename[selected_timestamp]]

if "scenarios" not in report: # OLD FORMAT
    report_scenarios = report
    services = None
else: # NEW FORMAT
    report_scenarios = report["scenarios"]
    services = report["services"]
    

test_results = defaultdict(lambda: defaultdict())

for scenario, content in report_scenarios.items():
    for operation, tests in content["operations"].items():
        for name, result in tests.items():
            test_results[name][(content["name"], operation)] = result

scenarios = [report_scenarios[scenario]["name"] for scenario in report_scenarios.keys()]
operations = list(reduce(lambda left, right: left.union(right), [set(content["operations"].keys()) for content in report_scenarios.values()], set()))
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

"""
### Tests Overview

* `Equations to AMR`: tests the ability to send a set of equations to `SKEMA` and to receive a valid AMR as response. Currently only LaTeX is tested.
* `Code to AMR`: tests the ability to send a code snippet (model core dynamics) to `SKEMA` and to receive a valid AMR as response. Currently only Python is tested.
* `PDF Extraction`: tests the ability to send a PDF’s text content to `SKEMA` and to receive metadata extractions and groundings in response.
* `Profile Dataset`: tests the ability to send a CSV dataset and corresponding documentation to `MIT` and to receive a “data card” in response.
* `PDF to Text`: tests the ability to send a PDF to `Cosmos` and to receive extracted text in response. 
* `Profile Model`: tests the ability to send a valid AMR and corresponding documentation to `MIT` and to receive a “model card” in response.

Currently tests are run against SKEMA, MIT and Cosmos public instances.
"""

if services is not None:
    st.write("### Service Info")
    service_names = list(services.keys())
    service_data = {
        "Service": service_names,
        "Source": [services[name]["source"] for name in service_names],
        "Version": [services[name]["version"] for name in service_names],
    }
    st.dataframe(pd.DataFrame(service_data), hide_index=True)


st.write("### Scenario Overview")
scenarios_overview = ""
for kk, vv in sorted(report_scenarios.items(), key=lambda item: item[1]['name']):
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