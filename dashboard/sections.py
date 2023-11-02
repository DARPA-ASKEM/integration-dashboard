from pyvis.network import Network
import networkx as nx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from dashboard.formatting import custom_title

# Function to apply styles
def highlight_empty(val):
    """
    Use with df = df.style.applymap(highlight_empty)
    This is a TODO we can implement later if we'd like
    """
    return 'background-color: #F8F8F8' if val == '' else ''

def render_scenario_viewer(scenarios):
    st.write(f"### Scenario Viewer")
    scenario_name = st.selectbox("Select a pipeline:", sorted(list(scenarios.keys())))
    scenario = scenarios[scenario_name]

    graph = nx.DiGraph()
    steps = scenario["steps"]
    total_time = 0
    for step_name, step_details in steps.items():
        # Check if the success value is "N/A" and skip this iteration
        if step_details["success"] == "N/A":
            continue
        
        total_time += step_details["time"] if step_details["time"] is not None else 0
        if step_details["success"] is not None:
            status_color = 'green' if step_details['success'] else 'red'
        else:
            status_color = 'gray'
        graph.add_node(step_name, color=status_color)
    shape = scenario["shape"]

    nx.set_node_attributes(graph, "box", "shape")
    pipeline = Network(notebook=False, directed=True)
    pipeline.from_nx(graph)
    for link in shape:
        # Ensure both nodes exist before adding an edge
        if link["from"] in graph.nodes and link["to"] in graph.nodes:
            # If the link is soft, set it to be dashed and gray
            if link["link_type"] == "soft":
                pipeline.add_edge(link["from"], link["to"], color="gray", dashes=True)
            else:
                pipeline.add_edge(link["from"], link["to"])

    pipeline.options = {
        'layout': {
            'hierarchical': {
                'enabled': False,
                'direction': 'LR',
                'sortMethod': 'directed'
            },
        },
    }
    display = pipeline.generate_html()

    
    st.write(f"**Scenario description**: `{scenario['description']}`")
    st.write(f"**Total Time** `{round(total_time,2)}`")
    st.write(">**Note**: tasks marked as grey were not run due to an upstream failure. " \
             "Solid lines indicated a `hard` dependency between the tasks. "\
             "Dashed lines indicate a `soft` dependency between the tasks meaning that "\
             "if results are available from the upstream task, they will be used (but are not required).")
    components.html(display, height=800, width=800)
    

def render_section_scenario_status(scenarios):
    st.write(f"### Scenario Status")
    status_data = {
        "Scenario": list(scenarios.keys()),
        "Success": [scenario["success"] for scenario in scenarios.values()], 
        "Total Time": [
            round(sum([step["time"] for step in scenario["steps"].values() if step["time"] is not None]),2) 
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
    df = df.sort_index(axis=0).sort_index(axis=1)
    return df
    
def render_section_integration_status(scenarios):
    st.write(f"### Integration Status")
    st.write(">**Note**: tasks are marked with a ✅ if they succeed and a ❌ if they fail. "\
             "⚪ indicates that a task was not run due to an upstream task failure. "\
            "Empty cells indicate that a task was not applicable/relevant to a given scenario.")
    df = get_feature_table(scenarios, "success")
    df.replace({False: "❌", True: "✅", "N/A": "", None: "⚪"}, inplace=True)  
    st.dataframe(df)

def render_section_time(scenarios):
    st.write(f"### Execution Time")
    st.write(f"Task execution time in seconds")
    df = get_feature_table(scenarios, "time")
    df = df.applymap(lambda t: round(t,2) if t is not None else None, ) # `df.round(2)` is ineffective
    df = df.replace([None, 0], "")
    df = df.fillna("")
    st.dataframe(df)


def render_section_accuracy(scenarios):
    st.write(f"### Accuracy")
    df = get_feature_table(scenarios, "accuracy")
    df = df.replace([None, 0], "")
    st.dataframe(df)

def render_section_errors(scenarios):
    st.write(f"### Error Logs")
    df_data = []
    for scenario_name, scenario_details in scenarios.items():
        row_data = {"Scenario": scenario_name}
        for step_name, step_details in scenario_details["steps"].items():
            if step_details["success"] == True or step_details["success"] == None:
                row_data[step_name] = ""            
            else:
                row_data[step_name] = step_details.get("result",{}).get("job_error","")
        df_data.append(row_data)
    df = pd.DataFrame(df_data)
    df.set_index("Scenario", inplace=True)
    df = df.sort_index(axis=0).sort_index(axis=1)
    st.dataframe(df)