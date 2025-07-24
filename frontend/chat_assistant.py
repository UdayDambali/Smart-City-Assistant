import streamlit as st
import requests

def render():
    st.subheader("🧠 Ask the Smart City Assistant")
    user_input = st.text_input("Ask a question")
    if st.button("Ask"):
        with st.spinner("Getting response..."):
            try:
                res = requests.post("http://localhost:8000/chat", json={"user_input": user_input}, timeout=15)
                res.raise_for_status()
                reply = res.json().get("response", "No reply")
            except Exception as e:
                reply = f"Error: {e}"
            st.write(reply)
