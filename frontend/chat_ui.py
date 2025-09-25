import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="HR Chatbot", page_icon="🤖")
st.title("🤖 HR Policy Chatbot")
st.write("Ask any question about the HR Policy document.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask me about HR policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = requests.post(API_URL, json={"question": prompt})
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "⚠️ No answer returned.").strip()
            sources = data.get("sources", [])
        else:
            answer, sources = f"⚠️ Backend error {response.status_code}", []
    except Exception as e:
        answer, sources = f"⚠️ Could not connect to backend: {e}", []

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.write(answer)
        if sources:
            st.markdown("**📚 Sources:**")
            for s in sources:
                st.write(f"- 📄 {s['title']} (Page {s['page']})")
