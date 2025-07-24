# Smart City Assistant

A modern, AI-powered dashboard for city sustainability, citizen engagement, and smart analytics.

## 🚀 Features

- **Dashboard Summary:**
  - City selection with real-time KPI metrics (water usage, energy, air quality, etc.)
- **Citizen Feedback:**
  - Submit feedback/issues with optional image upload
  - View all submitted feedback
- **Eco Tips:**
  - AI-powered eco-friendly tips and semantic search
- **KPI Forecasting:**
  - Time series forecasting of KPIs using Prophet
- **Anomaly Detection:**
  - Detect unusual spikes/drops in KPIs
- **Sustainability Report:**
  - Upload KPI data and generate detailed reports using Gemini AI
- **Policy Summarizer:**
  - Summarize policy documents (PDF, DOCX, TXT, or pasted text) with Gemini AI
- **Chat Assistant:**
  - Conversational AI assistant with session memory

## 🛠️ Tech Stack
- **Frontend:** Streamlit, streamlit-option-menu
- **Backend:** FastAPI (for chat, feedback, eco tips, etc.)
- **AI/ML:**
  - Google Gemini (google-generativeai)
  - Prophet (KPI forecasting)
  - Pinecone (semantic search, if enabled)
- **Data:** CSV files for KPIs and feedback
- **Other:** python-dotenv, PyPDF2, python-docx, matplotlib

## 📦 Setup

1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd SmartCity-Assistant
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the root directory with your API keys:
     ```env
     GEMINI_API_KEY=your_gemini_api_key
     WATSONX_API_KEY=your_watsonx_api_key
     PROJECT_ID=your_project_id
     MODEL_ID=your_model_id
     PINECONE_API_KEY=your_pinecone_api_key
     PINECONE_ENV=your_pinecone_env
     ```
4. **Run the backend (FastAPI):**
   ```bash
   uvicorn app.main:app --reload
   ```
5. **Run the frontend (Streamlit):**
   ```bash
   streamlit run frontend/smart_dashboard.py
   ```

## 📁 Data Files
- `data/kpi_data.csv` — KPI time series (must include city, kpi, value columns)
- `data/citizen_feedback.csv` — Feedback submissions
- `data/eco_tips.json` — Eco tips for semantic search

## 📝 Usage
- Use the sidebar to navigate between modules.
- Dashboard metrics update based on city selection and latest data.
- Upload files or paste text for reports and policy summaries.
- Feedback form supports image uploads.

## 🤖 AI Integrations
- **Gemini:** Used for report and policy summarization (requires API key)
- **Prophet:** Used for KPI forecasting
- **Pinecone:** Used for semantic eco tips (if enabled)

## 📚 Extending the Project
- Add more KPIs or cities by editing `data/kpi_data.csv`
- Add new modules or backend endpoints in `app/api/` and `app/services/`
- Customize UI in `frontend/smart_dashboard.py`

## 🧑‍💻 Contributors
- [Your Name]

## 📄 License
MIT License 
