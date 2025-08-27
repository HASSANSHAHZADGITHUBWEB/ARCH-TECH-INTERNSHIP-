import streamlit as st
import requests
import json

# Ollama API endpoint
OLLAMA_API = "http://localhost:11434/api/generate"

st.set_page_config(page_title="Local LLM with Ollama", page_icon="🤖", layout="wide")

st.title("🤖 Local LLM Chat (Ollama + Streamlit)")

# Conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar reset
if st.sidebar.button("🔄 Reset Conversation"):
    st.session_state.history = []

# Input + button
user_input = st.text_input("Type your message:")
submit = st.button("Send")

# Function to query Ollama
def query_ollama(prompt, model="llama2:7b"):
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            stream=True,
        )

        reply = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "message" in data and "content" in data["message"]:
                        reply += data["message"]["content"]
                except:
                    pass
        return reply.strip()
    except Exception as e:
        return f"⚠️ Error connecting to Ollama: {str(e)}"
