import streamlit as st
import requests
import os

# Get the API URL from environment variable or use default
API_URL = os.getenv("API_URL", "https://your-railway-app-url.up.railway.app")

st.set_page_config(page_title="RAG Chatbot")

st.title("📚 Production RAG Chatbot")

# Upload section
st.subheader("Upload Document")

uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

if uploaded_file:
    response = requests.post(
        f"{API_URL}/upload",
        files={"file": (uploaded_file.name, uploaded_file.getvalue())}
    )
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(f"Upload failed: {response.text}")

# Chat section
st.subheader("Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask something...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = requests.post(
        f"{API_URL}/ask",
        json={"question": prompt}
    )

    if response.status_code == 200:
        result = response.json()

        answer = result.get("answer", "Error")
        sources = result.get("sources", [])

        full_response = f"{answer}\n\n**Sources:** {sources}"

        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
    else:
        st.error(f"Failed to get response: {response.text}")