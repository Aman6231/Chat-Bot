import streamlit as st
import requests

# ---------- PAGE ----------
st.set_page_config(page_title="Custom AI Chatbot")
st.title("🤖 Custom AI Chatbot")

# ---------- LOAD KNOWLEDGE ----------
try:
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()
except:
    knowledge = "No knowledge file found."

# ---------- CHAT HISTORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------- USER INPUT ----------
question = st.chat_input("Ask a question")

if question:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.write(question)

    # Build prompt
    prompt = f"""
You are a helpful chatbot.

Answer using the information below.

Knowledge:
{knowledge}

Question:
{question}

Answer:
"""

    # Call Ollama
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False
            }
        )

        answer = response.json()["response"]

    except Exception:
        answer = """
Could not connect to Ollama.

Make sure Ollama is installed and running:

ollama run llama3.2
"""

    # Show assistant response
    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )