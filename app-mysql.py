import streamlit as st 
from dotenv import load_dotenv
import pandas as pd 
import os
from langchain_groq import ChatGroq
from pandasai import SmartDataframe
from pandasai.connectors import MySQLConnector

conn = MySQLConnector(
    config={
        "host":"localhost",
        "port":3306,
        "database":"genai",
        "username":"root",
        "password":"abcd1234",
        "table":"heart_disease",
        "table":"thyroid_disease"
    }
)

load_dotenv(override=True)

model = ChatGroq(
    temperature=0,
    model_name ="mixtral-8x7b-32768", 
    api_key = os.environ["GROQ_API_KEY"])

df_connector = SmartDataframe(conn, config={"llm": model})

st.title("Data Analysis with MySQL")

prompt = st.text_input("Enter your prompt:")

if st.button("Generate MySQL Response"):
    if prompt:
        with st.spinner("Generating response..."):
            st.write(df_connector.chat(prompt))

st.title("Data Analysis with CSV")

uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data.head(3))

    df = SmartDataframe(data, config={"llm": model})
    prompt = st.text_area("Enter your prompt:")

    if st.button("Generate CSV Response"):
        if prompt:
            with st.spinner("Generating response..."):
                st.write(df.chat(prompt))