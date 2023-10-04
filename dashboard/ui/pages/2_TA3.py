import json
import datetime
import os
import re
from functools import reduce
from collections import defaultdict

import streamlit as st
import pandas as pd

from dashboard.ui.utils.storage import select_report
from dashboard.ui.utils.formatting import custom_title


st.title("TA3 Integration Dashboard")

# Let the user select a report based on formatted timestamps
report = select_report("ta3")

report_scenarios = report["scenarios"]
services = report["services"]

st.sidebar.markdown("""
# TA3

TA3 integration status
""")

# """
# ### Tests Overview


# """

# if services is not None:
#     st.write("### Service Info")
#     service_names = list(services.keys())
#     service_data = {
#         "Service": service_names,
#         "Version": [services[name]["version"] for name in service_names],
#     }
#     st.dataframe(pd.DataFrame(service_data), hide_index=True)
proper_names = {
    "pyciemss": "PyCIEMSS",
    "sciml": "SciML"
}


for service in proper_names:
    test_results = defaultdict(lambda: defaultdict())

    for scenario, content in report_scenarios["scenarios"].items():
        for operation, tests in content["operations"].items():
            for name, result in tests.items():
                test_results[name][(content["name"], operation)] = result

    scenarios = list(report_scenarios[service].keys())
    operations = list(reduce(lambda left, right: left.union(right), [set(content["operations"].keys()) for content in report_scenarios[service].values()], set()))
    tests = sorted([i for i in test_results.keys()], reverse=True)
    dataframes = {name: pd.DataFrame(index=scenarios, columns=operations) for name in tests}


    st.write(f"### {proper_names[service]} Overview")
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