import streamlit as st 
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
import pandas as pd 
from pandasai import SmartDataframe
import os

load_dotenv(override=True)

model = ChatGroq(
    model ="mixtral-8x7b-32768", 
    api_key = os.environ["GROQ_API_KEY"])

st.title("Data Analysis with PandasAI")

uploaded_file = st.file_uploader("Upload a CSV file", type=['csv'])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data.head(3))

    df = SmartDataframe(data, config={"llm": model})
    prompt = st.text_area("Enter your prompt:")

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response..."):
                st.write(df.chat(prompt))