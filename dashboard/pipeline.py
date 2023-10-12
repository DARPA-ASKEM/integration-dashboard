from pyvis.network import Network
import networkx as nx
import pandas as pd
import streamlit as st

from dashboard.utils.formatting import custom_title

def create_pipeline(scenario):
    graph = nx.Graph()
    
    steps = scenario_data["steps"]
    for step_name, step_details in steps.items():
        status_color = 'green' if step_details['status'] == 'finished' else 'red'
        graph.add_node(step_name, color=status_color)
    
    shape = scenario_data["shape"]
    for link in shape:
        graph.add_edge(link["from"], link["to"])
    
    pipeline = Network(notebook=True, directed=True)
    pipeline.from_nx(graph)
    return pipeline


def render_section_pipeline(report):
    st.write(f"### Flow Viewer")
    scenarios = report["scenarios"]
    scenario_name = st.selectbox("Select a pipeline:", list(scenarios.keys()))
    pipeline = create_pipeline(scenario[scenario_name])
    st.write(pipeline.html, unsafe_allow_html=True)
    

def render_section_integration_status(report):
    st.write(f"### Integration Status")
    scenarios = report["scenarios"]
    statuses = pd.Series({ name: scenario["status"] for name, scenario in scenarios.items() })
    statuses.replace({False: "❌", True: "✅", None: ""}, inplace=True)
    status.rename(custom_title)
    st.dataframe(status)
