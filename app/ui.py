import streamlit as st
import requests

API_URL = "http://localhost:8000"

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
    st.success(response.json()["message"])

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
        f"{API_URL}/chat",
        json={"question": prompt}
    )

    result = response.json()

    answer = result.get("answer", "Error")
    sources = result.get("sources", [])

    full_response = f"{answer}\n\n**Sources:** {sources}"

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )

    st.rerun()