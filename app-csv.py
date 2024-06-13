import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from pandasai import SmartDataframe

load_dotenv(override=True)

# Groq LLM Configuration
def load_groq_llm():
    return ChatGroq(model_name='llama3-8b-8192', api_key=os.environ['GROQ_API_KEY'])

# Main App Logic
def main():
    st.title("Data Analysis with CSV")

    # File Upload
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        llm = load_groq_llm()
        df = SmartDataframe(data, config={'llm': llm})

        # Chat Interactions
        query = st.text_input("Enter your query about the data:")
        if query:
            response = df.chat(query)
            st.write(response)

if __name__ == "__main__":
    main()