import json
import datetime
import os
from functools import reduce
from collections import defaultdict

import streamlit as st
import pandas as pd

from dashboard.utils.storage import select_report
from dashboard.utils.formatting import custom_title
from dashboard.sections import render_section_integration_status, render_section_pipeline, render_section_time, render_section_accuracy

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
st.write("### Service Info")
service_names = list(services.keys())
service_data = {
    "Service": service_names,
    "Source": [services[name]["source"] for name in service_names],
    "Version": [services[name]["version"] for name in service_names],
}
st.dataframe(pd.DataFrame(service_data), hide_index=True)


st.write("### Scenario Overview")
"TODO"

render_section_integration_status(report)
# render_section_time(report)
# render_section_accuracy(report)
render_section_pipeline(report)