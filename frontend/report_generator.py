import streamlit as st
import requests

def render():
    st.subheader("📄 City Sustainability Report")
    city_name = st.text_input("Enter City Name")
    if st.button("Generate Report"):
        res = requests.post("http://localhost:8000/chat/report", json={"city": city_name})
        st.text_area("Report", res.json().get("report", ""), height=400)
