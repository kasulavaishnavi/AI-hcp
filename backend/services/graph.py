from langgraph.graph import StateGraph, END

from services.agent import run_agent


# Agent Node
def agent_node(state):

    user_input = state["input"]

    result = run_agent(user_input)

    return {
        "result": result
    }


# Build LangGraph
def build_graph():

    builder = StateGraph(dict)

    # Single AI workflow node
    builder.add_node("agent", agent_node)

    # Flow
    builder.set_entry_point("agent")

    builder.add_edge("agent", END)

    return builder.compile()


# Final Graph
graph = build_graph()