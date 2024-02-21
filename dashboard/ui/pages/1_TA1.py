import json
import datetime
import os
from functools import reduce
from collections import defaultdict

import streamlit as st
import pandas as pd

from dashboard.storage import select_report
from dashboard.formatting import custom_title
from dashboard.sections import (
    render_scenario_viewer,
    render_section_scenario_status, 
    render_section_integration_status, 
    render_section_time, 
    render_section_accuracy,
    render_section_errors
)

st.title("TA1 Integration Dashboard")

st.write("Whenever the test harness is run, the various assets are published to the `Integration Test Suite` project in Terarium."\
         " Click below to view the report results in Terarium.")
st.link_button("View report assets in Terarium", "https://app.terarium.ai/projects/102/overview")

st.divider()

report = select_report("ta1")

# Download report button
st.download_button(
    label="Download report `json`",
    data=json.dumps(report, indent=4).encode('utf-8'),
    file_name="report.json",
    mime="application/json"
)

st.sidebar.markdown("""
# TA1

TA1 integration status and quality metrics.
""")

services = report["services"]
st.write("## Service Info")
st.write(">**Note**: if the `Version` for any service is unavailable it indicates that the report"\
         "runner was unable to communicate with the service. In that case, substantial failures"\
         "are expected across the board.")
service_names = list(services.keys())
service_data = {
    "Service": service_names,
    "Source": [services[name]["source"] for name in service_names],
    "Version": [services[name]["version"] for name in service_names],
}
st.dataframe(pd.DataFrame(service_data), hide_index=True)

st.write("## Tasks Overview")
tasks = {
    "Code to AMR": "SKEMA: Convert a repository or annotated dynamics into an AMR.",
    "Equations to AMR": "SKEMA: Convert LaTeX or Presentation MathML to a Petrinet or Regulatory Network AMR.",
    "Link AMR": "SKEMA/MIT: Link an AMR to extracted variables in order to 'enrich' the AMR.",
    "PDF Extraction": "COSMOS: Perform table, text and figure extraction over a PDF paper.",
    "Profile Dataset":"MIT: Analyze a structured dataset by examining the provided sample and its description. This process aims to gain insights into its schema, contents, and column-specific statistics.",
    "Profile Model": "MIT: Evaluate a model through an in-depth review of its code and description. This includes understanding aspects such as authorship, schema, provenance, and usage.",
    "Variable Extraction": "SKEMA/MIT: Identify and extract variables from scientific papers. This involves mapping these variables to the relevant dataset, grounding them in a knowledge graph, and gathering additional pertinent information."
        }

# Convert the dictionary into a list of tuples (key-value pairs)
tasks_data = list(tasks.items())
# Create the DataFrame
tasks_df = pd.DataFrame(tasks_data, columns=["Task Name", "Task Description"])
st.dataframe(tasks_df, hide_index=True)


scenarios = report["scenarios"]

st.write("## Testing")
render_section_scenario_status(scenarios)
render_section_integration_status(scenarios)
render_section_time(scenarios)
render_section_accuracy(scenarios)
render_section_errors(scenarios)
render_scenario_viewer(scenarios)