from pyvis.network import Network
import networkx as nx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from dashboard.formatting import custom_title


def render_section_scenario(scenarios):
    st.write(f"### Flow Viewer")
    scenario_name = st.selectbox("Select a pipeline:", list(scenarios.keys()))
    scenario = scenarios[scenario_name]

    graph = nx.DiGraph()
    steps = scenario["steps"]
    total_time = 0
    for step_name, step_details in steps.items():
        total_time += step_details["time"]
        status_color = 'green' if step_details['success'] else 'red'
        graph.add_node(step_name, color=status_color)
    shape = scenario["shape"]
    for link in shape:
        graph.add_edge(link["from"], link["to"])
    pipeline = Network(notebook=False, directed=True)
    pipeline.from_nx(graph)
    display = pipeline.generate_html()

    
    st.write("""
        ### Scenario Description
        TODO: RENDER ONCE IT'S PROVIDED
    """)
    st.metric("Total Time", total_time)
    components.html(display, height=800, width=800)
    

def render_section_scenario_status(scenarios):
    st.write(f"### Scenario Status")
    status_data = {
        "Scenario": list(scenarios.keys()),
        "Success": [scenario["success"] for scenario in scenarios.values()], 
        "Total Time": [
            sum([step["time"] for step in scenario["steps"].values()]) 
            for scenario in scenarios.values()
        ]
    }
    df = pd.DataFrame(status_data)
    df.replace({False: "❌", True: "✅"}, inplace=True)
    st.dataframe(df, hide_index=True)

    
def get_feature_table(scenarios, feature):
    results = {}
    step_names = set()
    for scenario_name, scenario in scenarios.items():
        for step_name, step in scenario["steps"].items():
            step_names.add(step_name)
            results[(scenario_name, step_name)] = step[feature]
    df = pd.DataFrame(index=list(scenarios.keys()), columns=list(step_names))
    for (scenario_name, step_name), result in results.items():
        df.at[scenario_name, step_name] = result
    return df
    
def render_section_integration_status(scenarios):
    st.write(f"### Integration Status")
    df = get_feature_table(scenarios, "success")
    df.replace({False: "❌", True: "✅", None: ""}, inplace=True)
    st.dataframe(df, hide_index=True)

def render_section_time(scenarios):
    st.write(f"### Execution Time")
    df = get_feature_table(scenarios, "time")
    st.dataframe(df, hide_index=True)


def render_section_accuracy(scenarios):
    st.write(f"### Accuracy")
    df = get_feature_table(scenarios, "accuracy")
    st.dataframe(df, hide_index=True)
