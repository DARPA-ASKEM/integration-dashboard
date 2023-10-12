from pyvis.network import Network
import networkx as nx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from dashboard.utils.formatting import custom_title


def render_section_pipeline(report):
    st.write(f"### Flow Viewer")
    scenarios = report["scenarios"]
    scenario_name = st.selectbox("Select a pipeline:", list(scenarios.keys()))
    scenario = scenarios[scenario_name]

    graph = nx.Graph()
    steps = scenario["steps"]
    for step_name, step_details in steps.items():
        status_color = 'green' if step_details['success'] else 'red'
        graph.add_node(step_name, color=status_color)
    shape = scenario["shape"]
    for link in shape:
        graph.add_edge(link["from"], link["to"])
    pipeline = Network(notebook=False, directed=True)
    pipeline.from_nx(graph)
    display = pipeline.generate_html()
    components.html(display, height=800, width=800)
    

def render_section_integration_status(report):
    st.write(f"### Integration Status")
    scenarios = report["scenarios"]
    statuses = pd.Series({ name: scenario["success"] for name, scenario in scenarios.items() })
    statuses.replace({False: "❌", True: "✅", None: ""}, inplace=True)
    statuses.rename(custom_title)
    st.dataframe(statuses)

    
def render_section_time(report):
    st.write(f"### Execution Time")
    scenarios = report["scenarios"]
    times = pd.Series({ name: scenario["time"] for name, scenario in scenarios.items() })
    times.rename(custom_title)
    st.dataframe(times, hide_index=True)


def render_section_accuracy(report):
    st.write(f"### Accuracy")
    scenarios = report["scenarios"]
    accuracies = pd.Series({ name: scenario["accuracy"] for name, scenario in scenarios.items() })
    accuracies.rename(custom_title)
    st.dataframe(accuracies)
