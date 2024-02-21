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
    "Code to AMR": "SKEMA: Extracts equations and models from a codebase or code snippet. A code collection or code snippet (Python, Fortran) is provided as input and the SKEMA Code2FN pipeline interprets the code as a Function Network; SKEMA MORAE then attempts to identify the core dynamics, interpret it as a supported model type, and outputs a serialized AMR.",
    "Equations to AMR": "SKEMA: Extracts AMR from a set of input equations. Each input equation is assumed to be a single equation expression. The input representations may be equation images, LaTeX or Presentation MathML. The input representations are converted into the internal SKEMA MathExpressionTree representation; this is further interpreted as a representation of a supported model framework type and output as a serialized AMR.",
    "Link AMR": "SKEMA/MIT: Given an AMR and a set of variable extractions, this task uses the SKEMA alignment service to link the elements (states and parameters) of the AMR to the variable extractions. Matching is primarily driven by text embedding similarity, but for elements that lack descriptions, the alignment will use a set of heuristics depending on the AMR subtype.",
    "PDF Extraction": "COSMOS: Given an input pdf file, this task (1) extracts the text using the COSMOS endpoint, then (2) runs the SKEMA Text Reading service to extract variable descriptions, variables with values, variable units, and scenario context from the text. Optionally the MIT extractions are also collected and integrated. Output consists of a unified JSON format that includes all of the extractions.",
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