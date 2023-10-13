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
    render_section_accuracy
)

st.title("TA1 Integration Dashboard")


report = select_report("ta1")

st.sidebar.markdown("""
# TA1

TA1 integration status and quality metrics.
""")

"""
### Tests Overview
TODO
"""

services = report["services"]
st.write("## Service Info")
service_names = list(services.keys())
service_data = {
    "Service": service_names,
    "Source": [services[name]["source"] for name in service_names],
    "Version": [services[name]["version"] for name in service_names],
}
st.dataframe(pd.DataFrame(service_data), hide_index=True)


scenarios = report["scenarios"]

st.write("## Testing")
render_section_scenario_status(scenarios)
render_section_integration_status(scenarios)
render_section_time(scenarios)
render_section_accuracy(scenarios)
render_scenario_viewer(scenarios)
