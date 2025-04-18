import streamlit as st
import pandas as pd
from openai import OpenAI

# Streamlit page config
st.set_page_config(page_title="Middleware Log Root Cause Analyzer", layout="wide")

st.title("🛠️ Middleware Log Root Cause Analyzer with GPT")
st.markdown("Upload middleware logs (e.g., WebLogic, WebSphere, Tomcat) and let GPT identify the **root cause**.")

# API key input
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# File upload
uploaded_file = st.file_uploader("📄 Upload your middleware log file (.log or .txt)", type=["log", "txt"])

# Main logic
if uploaded_file and api_key:
    try:
        client = OpenAI(api_key=api_key)

        with st.spinner("Analyzing middleware log... 🤖"):
            log_data = uploaded_file.read().decode("utf-8")

            prompt = f"""
            You are a middleware and infrastructure expert. Analyze the following middleware server log
            (e.g., WebLogic, WebSphere, Tomcat, or similar) and identify the **root cause** of any critical errors,
            startup failures, deployment issues, or configuration problems.

            Provide:
            - A short summary of the root cause (if any).
            - Suggested action steps to resolve the issue.
            - Any patterns or recurring errors worth noting.

            Log:
            {log_data}
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful middleware support assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )

            answer = response.choices[0].message.content
            st.success("✅ Analysis complete!")
            st.subheader("🧠 Root Cause Analysis")
            st.write(answer)

    except Exception as e:
        error_message = str(e)
        if "Unauthorized" in error_message or "Invalid" in error_message:
            st.error("❌ Invalid OpenAI API Key.")
        else:
            st.error(f"🚨 Unexpected error: {error_message}")
