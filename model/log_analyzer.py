# streamlit_app.py

import streamlit as st
import requests
import google.generativeai as genai

# Load Gemini Key
genai.configure(api_key="AIzaSyDdJW2e5eGpsHdLVRKKqJzuOSPKRpphWN8")

st.set_page_config(page_title="Data Breach Analyzer", layout="wide")
st.title("📊 Employee Access Log Analyzer (via Gemini)")

# Step 1: Fetch logs from your Express API
with st.spinner("Fetching logs..."):
    response = requests.get("http://localhost:1111/logs")
    logs = response.json()

# Step 2: Display raw logs
if st.checkbox("Show Raw Logs"):
    st.json(logs)

# Step 3: Send logs to Gemini for anomaly detection
prompt = f"""
You are a data breach detection system and access log intelligence analyst.

Analyze the following employee access logs to generate a detailed report with:

1. Suspicious or anomalous patterns:
   - Accessing sensitive systems at odd hours (e.g., midnight, weekends).
   - High number of accesses in a short time (burst behavior).
   - Frequent access to specific files or systems within a single day.

2. Identify employees or departments showing abnormal behavior.

3. Justify each anomaly with reasons — e.g., "Accessed 5+ times in 10 minutes", "Accessed 3 systems not used by anyone else in this department", "Repeated file access every hour".

4. Output the result in:
   - A **summary of threats**
   - A **table** of potential breaches with columns:
     Emp_name | Dept_Name | Date_Time | Reason

Logs:
{logs}
"""

with st.spinner("Analyzing logs using Gemini..."):
    model = genai.GenerativeModel(model_name='models/gemini-1.5-pro')
    result = model.generate_content(prompt)
    analysis = result.text

# Step 4: Display Analysis
st.subheader("🛡️ Gemini AI Breach Report")
st.markdown(analysis)
