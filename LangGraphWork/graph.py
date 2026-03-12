from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from state import AgentState
from utils.helpers import get_llm
from tools.file_tools import ALL_TOOLS

# 1. Define Tools and Bind the Model
tools = ALL_TOOLS
llm = get_llm().bind_tools(tools)

# 2. Define Nodes
def call_model(state: AgentState):
    """Node where the LLM makes a decision"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build the Graph Workflow
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("agent", call_model)
# ToolNode is a pre-built structure that allows LangGraph to run tools automatically
workflow.add_node("tools", ToolNode(tools))

# Set the Entry Point
workflow.set_entry_point("agent")

# 4. Define Logical Transitions (Edges)
def should_continue(state: AgentState):
    """Does the LLM want to use a tool or provide a final answer?"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "continue"
    return "end"

# Add Conditional Edges
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END
    }
)

# After tools run, always return to the 'agent' (Loop)
workflow.add_edge("tools", "agent")

# 5. Compile the Graph
app = workflow.compile()