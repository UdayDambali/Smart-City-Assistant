import streamlit as st
from streamlit_option_menu import option_menu
import requests
import pandas as pd
from datetime import datetime
import os
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
# import plotly.express as px
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2
import docx
import binascii
import pdfplumber

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

feedback_file = "data/citizen_feedback.csv"
os.makedirs("data", exist_ok=True)

def clear_input():
    st.session_state.chat_input = ""

def generate_sustainability_report_gemini(kpi_summary, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f'''
    Generate a detailed sustainability report based on the following KPI summary:

    {kpi_summary}

    Include:
    - Overview of current performance
    - Areas of concern
    - Suggestions for improvement
    - Positive achievements
    '''
    response = model.generate_content(prompt)
    return response.text

def extract_text_from_pdf(file):
    text = ""
    try:
        print("[DEBUG] Trying PyPDF2 extraction...")
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    except (binascii.Error, PyPDF2.errors.PdfReadError) as e:
        print(f"[DEBUG] PyPDF2 failed: {e}. Trying pdfplumber fallback...")
        try:
            file.seek(0)
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e2:
            print(f"[DEBUG] pdfplumber also failed: {e2}")
            text = "Error: The uploaded file may be corrupted or not a valid PDF."
    except Exception as e:
        print(f"[DEBUG] General error in PDF extraction: {e}")
        text = f"Error: {e}"
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# --- Sidebar Navigation ---
with st.sidebar:
    selected = option_menu(
        "Smart City Assistant",
        [
            "Dashboard Summary",
            "Citizen Feedback",
            "Eco Tips",
            "KPI Forecasting",
            "Anomaly Detection",
            "Sustainability Report",
            "Policy Summarizer",
            "Chat Assistant"
        ],
        icons=[
            "bar-chart", "chat-left-text", "tree", "graph-up", 
            "exclamation-triangle", "file-earmark-text", 
            "journal-text", "robot"
        ],
        menu_icon="house-fill",
        default_index=0,
        styles={
            "container": {"padding": "8px", "background-color": "#181c25", "border-radius": "16px"},
            "icon": {"color": "#4ade80", "font-size": "22px"},
            "nav-link": {
                "font-size": "17px", "text-align": "left", "margin": "6px",
                "color": "#e5e7eb", "border-radius": "8px",
                "font-weight": "500",
                "--hover-color": "#23293a"
            },
            "nav-link-selected": {"background-color": "#4ade80", "color": "#181c25", "font-weight": "700"},
        }
    )

# --- Main Content Area ---
if selected == "Dashboard Summary":
    st.markdown(f"<h2 style='text-align:center;'>Smart Dashboard</h2>", unsafe_allow_html=True)
    city = st.selectbox(
        "🌆 City",
        [
            "Pune", "Mumbai", "Delhi", "Chennai", "Bengaluru", "Hyderabad", "Ahmedabad", "Jaipur", "Kolkata", "Lucknow", "Surat", "Chandigarh", "Bhopal", "Indore"
        ],
        index=0
    )
    # Try to load city KPI data
    kpi_file = "data/kpi_data.csv"
    water_usage = energy_usage = air_quality = "N/A"
    if os.path.exists(kpi_file):
        df = pd.read_csv(kpi_file)
        # Try to get the latest data for the selected city
        city_df = df[df.get('city', city) == city] if 'city' in df.columns else df
        # Get latest date row for each KPI
        for kpi, var in [("water_usage", "water_usage"), ("energy_usage", "energy_usage"), ("air_quality", "air_quality")]:
            kpi_rows = city_df[city_df["kpi"] == kpi]
            if not kpi_rows.empty:
                latest_row = kpi_rows.sort_values("date").iloc[-1]
                if kpi == "water_usage":
                    water_usage = latest_row["value"]
                elif kpi == "energy_usage":
                    energy_usage = latest_row["value"]
                elif kpi == "air_quality":
                    air_quality = latest_row["value"]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="💧 Water Usage", value=water_usage)
    with col2:
        st.metric(label="⚡ Energy Consumption", value=energy_usage)
    with col3:
        st.metric(label="🌫️ Air Quality Index", value=air_quality)

elif selected == "Citizen Feedback":
    st.markdown("## 📝 Submit Your Feedback or Report an Issue")
    st.markdown("Help us make the city better! Your feedback matters.")

    import uuid
    feedback_file = "data/citizen_feedback.csv"
    os.makedirs("data/feedback_images", exist_ok=True)

    with st.form("feedback_form"):
        name = st.text_input("👤 Your Name")
        issue_type = st.selectbox("📌 Type of Issue", ["Garbage", "Water", "Electricity", "Noise", "Others"])
        description = st.text_area("📝 Describe the issue or suggestion")
        image = st.file_uploader("📷 Upload an image (optional)", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("🚀 Submit")
        image_filename = ""
        if submitted:
            if image:
                image_id = str(uuid.uuid4())
                ext = image.name.split('.')[-1]
                image_filename = f"data/feedback_images/{image_id}.{ext}"
                with open(image_filename, "wb") as f:
                    f.write(image.read())
            new_feedback = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name,
                "issue_type": issue_type,
                "description": description,
                "image": image_filename
            }
            # Save to CSV
            if os.path.exists(feedback_file):
                df = pd.read_csv(feedback_file)
                df = pd.concat([df, pd.DataFrame([new_feedback])], ignore_index=True)
            else:
                df = pd.DataFrame([new_feedback])
            df.to_csv(feedback_file, index=False)
            st.success("✅ Thank you for your feedback!")
            if image_filename:
                st.image(image_filename, caption="Uploaded Image", use_column_width=True)

    with st.expander("📂 View Submitted Feedback"):
        if os.path.exists(feedback_file):
            df = pd.read_csv(feedback_file)
            st.dataframe(df)
        else:
            st.info("No feedback submitted yet.")

elif selected == "Eco Tips":
    st.markdown("<h2 style='display:flex;align-items:center;'>🌿 <span style='margin-left:8px;'>Eco-Friendly Tips Assistant</span></h2>", unsafe_allow_html=True)
    # Optionally, display a custom logo image if available
    # st.image('frontend/assets/eco_logo.png', width=48)
    st.markdown("Get actionable suggestions to live sustainably based on your query.")
    query = st.text_input("💬 Enter a topic (e.g., recycling, energy, water, plastic):")
    if st.button("🌱 Get Eco Tip"):
        if query:
            # Replace this with real Pinecone/LLM API call
            st.success(f"🔍 Tip for **{query.title()}**: Reduce usage of {query}, reuse what you can, and recycle the rest.")
        else:
            st.warning("⚠️ Please enter a topic.")

elif selected == "KPI Forecasting":
    st.markdown("## 📊 KPI Forecasting")
    st.write("Forecast key performance indicators like electricity usage, pollution, etc.")

    data_file = "data/kpi_data.csv"
    if not os.path.exists(data_file):
        st.error("KPI data not found.")
    else:
        df = pd.read_csv(data_file)
        kpi_options = df['kpi'].unique().tolist()
        
        selected_kpi = st.selectbox("🔍 Select KPI to Forecast", kpi_options)
        forecast_period = st.slider("⏱ Months to Forecast", 1, 12, 6)

        # Filter for selected KPI
        kpi_df = df[df['kpi'] == selected_kpi][['date', 'value']]
        kpi_df.columns = ['ds', 'y']  # Prophet format
        kpi_df['ds'] = pd.to_datetime(kpi_df['ds'])

        # Forecast using Prophet
        model = Prophet()
        model.fit(kpi_df)
        future = model.make_future_dataframe(periods=forecast_period, freq='MS')
        forecast = model.predict(future)

        # Plot
        fig1 = model.plot(forecast)
        st.pyplot(fig1)

        with st.expander("📄 View Forecast Data"):
            st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(forecast_period))

elif selected == "Anomaly Detection":
    st.markdown("## 🚨 Anomaly Detection")
    st.write("Detect unusual spikes or drops in your KPIs (e.g., leakage, outage, pollution spike).")

    # Load data
    df = pd.read_csv("data/kpi_data.csv", parse_dates=["date"])

    # User selects KPI
    kpi_type = st.selectbox("Select KPI", df["kpi"].unique())

    # Filter data
    kpi_df = df[df["kpi"] == kpi_type].sort_values("date")

    # Compute rolling stats
    window = st.slider("Rolling Window (months)", 2, 6, 3)
    rolling_mean = kpi_df["value"].rolling(window=window).mean()
    rolling_std = kpi_df["value"].rolling(window=window).std()

    # Detect anomalies (2 standard deviations from rolling mean)
    kpi_df["anomaly"] = abs(kpi_df["value"] - rolling_mean) > 2 * rolling_std

    # Show line chart with anomalies
    st.line_chart(kpi_df.set_index("date")["value"])
    st.write("🚨 Anomalies Detected:")
    st.dataframe(kpi_df[kpi_df["anomaly"]])

elif selected == "Sustainability Report":
    st.markdown("## 🌱 Sustainability Report Generator")
    st.write("Upload your city KPI data (CSV/Excel) to generate a detailed sustainability report using Gemini AI.")

    # Use API key from .env
    api_key = GEMINI_API_KEY
    if not api_key:
        st.error("GEMINI_API_KEY not found in .env file.")
    else:
        uploaded_file = st.file_uploader("Upload KPI Data (CSV or Excel)", type=["csv", "xlsx"])

        report = None
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.dataframe(df)

            # Summarize data (simple: describe, or customize as needed)
            kpi_summary = df.describe(include='all').to_string()

            if st.button("Generate Sustainability Report"):
                with st.spinner("Generating report with Gemini..."):
                    try:
                        report = generate_sustainability_report_gemini(kpi_summary, api_key)
                        st.markdown("### 📝 Sustainability Report")
                        st.write(report)
                        st.session_state.generated_report = report
                    except Exception as e:
                        st.error(f"Error generating report: {e}")

        # Download as Markdown
        if "generated_report" in st.session_state and st.session_state.generated_report:
            st.download_button(
                label="Download Report as Markdown",
                data=st.session_state.generated_report,
                file_name="sustainability_report.md",
                mime="text/markdown"
            )

elif selected == "Policy Summarizer":
    st.markdown("## 📄 Policy Summarizer")
    st.write("Upload a policy file (PDF, DOCX, TXT) or paste text below to get a summary powered by Gemini AI.")

    uploaded_file = st.file_uploader("Upload Policy File (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    policy_text = ""
    if uploaded_file:
        print("[DEBUG] File name:", uploaded_file.name)
        print("[DEBUG] File type:", uploaded_file.type)
        print("[DEBUG] File size:", uploaded_file.size)
        if uploaded_file.name.endswith(".pdf"):
            uploaded_file.seek(0)
            file_bytes = uploaded_file.read()
            print("[DEBUG] First 20 bytes:", file_bytes[:20])
            uploaded_file.seek(0)
            policy_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            policy_text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            policy_text = uploaded_file.read().decode("utf-8")
        st.success("File loaded! You can edit the extracted text below if needed.")
    policy_text = st.text_area("Policy Text", value=policy_text, height=200)

    summary = None
    if st.button("Summarize Policy"):
        if not policy_text.strip():
            st.warning("Please provide some policy text to summarize.")
        else:
            api_key = GEMINI_API_KEY
            if not api_key:
                st.error("GEMINI_API_KEY not found in .env file.")
            else:
                with st.spinner("Summarizing policy with Gemini..."):
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        prompt = f"""
                        Summarize the following city policy for a general audience. Focus on the main goals, actions, and expected outcomes.\n\nPolicy:\n{policy_text}
                        """
                        response = model.generate_content(prompt)
                        summary = response.text
                        st.markdown("### 📝 Policy Summary")
                        st.write(summary)
                        st.session_state.policy_summary = summary
                    except Exception as e:
                        st.error(f"Error summarizing policy: {e}")
    if "policy_summary" in st.session_state and st.session_state.policy_summary:
        st.download_button(
            label="Download Summary as Markdown",
            data=st.session_state.policy_summary,
            file_name="policy_summary.md",
            mime="text/markdown"
        )

elif selected == "Chat Assistant":
    st.markdown("## 🤖 Smart City Chat Assistant")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message", key="chat_input")
        send = st.form_submit_button("Send")
        if send and user_input:
            with st.spinner("Assistant is typing..."):
                try:
                    res = requests.post(
                        "http://localhost:8000/chat",
                        json={
                            "user_input": user_input,
                            "chat_history": st.session_state.chat_history
                        },
                        timeout=15
                    )
                    res.raise_for_status()
                    reply = res.json().get("response", "No reply")
                except Exception as e:
                    reply = f"Error: {e}"
                st.session_state.chat_history.append(("user", user_input))
                st.session_state.chat_history.append(("assistant", reply))

    # Display chat history
    for sender, message in st.session_state.chat_history:
        if sender == "user":
            st.markdown(f"<div style='text-align:right; color:#4ade80;'><b>You:</b> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; color:#fff; background:#23293a; border-radius:8px; padding:8px; margin-bottom:4px;'><b>Assistant:</b> {message}</div>", unsafe_allow_html=True)
