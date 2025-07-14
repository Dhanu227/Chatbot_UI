from chatbot.graph import build_graph

def chat():
    graph = build_graph()
    state = {"messages": []}
    print("\n🤖 Chatbot ready! Type 'exit' to quit.\n")
    while True:
        msg = input("You: ")
        if msg.strip().lower() == "exit":
            break
        state["messages"].append({"role": "user", "content": msg})
        state = graph.invoke(state)
        reply = state["messages"][-1]["content"]
        print(f"Assistant: {reply}\n")

if __name__ == "__main__":
    chat()
