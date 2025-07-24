import streamlit as st
import requests

def render():
    st.title("🌍 Eco Tips Assistant")

    tab1, tab2 = st.tabs(["🔄 Static Tips", "🔍 Semantic Search"])

    # -------- Tab 1: Static Eco Tips --------
    with tab1:
        st.subheader("🌱 Sustainable Eco Tips (Static)")
        
        if st.button("🔁 Refresh Tips"):
            with st.spinner("Fetching static tips..."):
                try:
                    res = requests.get("http://localhost:8000/get-eco-tips", timeout=30)
                    tips = res.json().get("tips", [])
                except Exception as e:
                    st.error(f"Failed to load tips: {e}")
                    return

                if tips:
                    st.success("Here are your eco-friendly tips:")
                    for tip in tips:
                        st.markdown(f"✅ **{tip['tip']}** (_{tip['category']}_)")
                else:
                    st.warning("No tips found.")

    # -------- Tab 2: Semantic Search Tips --------
    with tab2:
        st.subheader("🔍 Search Eco Tips (AI-Powered)")

        query = st.text_input("Enter your eco-related query:")

        if query:
            with st.spinner("Searching tips..."):
                try:
                    res = requests.get("http://localhost:8000/semantic-eco-tips", params={"query": query})
                    results = res.json().get("results", [])
                    if results:
                        st.success("Here are the most relevant eco tips:")
                        for tip in results:
                            st.markdown(f"✅ **{tip['tip']}** (_{tip['category']}_)")
                    else:
                        st.warning("No similar tips found.")
                except Exception as e:
                    st.error(f"Error fetching semantic tips: {e}")

