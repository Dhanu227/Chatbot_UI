from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict
from chatbot.llm import generate_response

# 1. Define the state schema
class ChatState(TypedDict):
    messages: List[Dict[str, str]]

# 2. Define the node logic
def chatbot_node(state: ChatState) -> ChatState:
    user_message = state["messages"][-1]["content"]
    reply = generate_response(state["messages"])
    state["messages"].append({"role": "assistant", "content": reply})
    return state

# 3. Build the graph
def build_graph():
    workflow = StateGraph(ChatState)

    workflow.add_node("chatbot", chatbot_node)
    workflow.set_entry_point("chatbot")

    # ✅ No need to explicitly call `add_edge("chatbot", END)`
    # Just set finish point as the last node
    workflow.set_finish_point("chatbot")  # not END

    return workflow.compile()
