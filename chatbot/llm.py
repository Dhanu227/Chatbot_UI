from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="mistral:7b")

def generate_response(messages):
    prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
    return llm.invoke(prompt)
