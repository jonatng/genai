import streamlit as st
from groq import Groq
import pandas as pd
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from pandasai import SmartDataframe

load_dotenv(override=True)

# Groq LLM Configuration
load_groq_llm = ChatGroq(
    model_name="llama3-8b-8192", 
    api_key=st.secrets['GROQ_API_KEY'])

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
    
# Phase 2 to include multiple LLMs, temperature, UI enhancements
# st.set_page_config(page_icon="💬", layout="wide",
#                    page_title="Data Analysis")

# def icon(emoji: str):
#     """Shows an emoji as a Notion-style page icon."""
#     st.write(
#         f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
#         unsafe_allow_html=True,
#     )

# icon("🔎")

# st.subheader("Data Analysis", divider="rainbow", anchor=False)

# client = Groq(
#     api_key=st.secrets["GROQ_API_KEY"],
# )

# # Initialize chat history and selected model
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "selected_model" not in st.session_state:
#     st.session_state.selected_model = None

# models = {
#     "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
#     "llama3-70b-8192": {"name": "llama3-8b-8192", "tokens": 8192, "developer": "Meta"},
#     "llama3-8b-8192": {"name": "llama3-8b-8192", "tokens": 8192, "developer": "Meta"},
#     "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"}
# }

# # Layout for model selection and max_tokens slider
# col1, col2 = st.columns(2)

# with col1:
#     model_option = st.selectbox(
#         "Choose a model:",
#         options=list(models.keys()),
#         format_func=lambda x: models[x]["name"],
#         index=3  # Default to mixtral
#     )

# # Detect model change and clear chat history if model has changed
# if st.session_state.selected_model != model_option:
#     st.session_state.messages = []
#     st.session_state.selected_model = model_option
    
# max_tokens_range = models[model_option]['tokens']

# with col2:
#     # Adjust max_tokens slider dynamically based on the selected model
#     max_tokens = st.slider(
#         "Max Tokens:",
#         min_value=512,  # Minimum value to allow some flexibility
#         max_value=max_tokens_range,
#         # Default value or max allowed if less
#         value=min(32768, max_tokens_range),
#         step=512,
#         help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
#     )

# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     avatar = '🤖' if message['role'] == 'assistant' else '👨‍💻'
#     with st.chat_message(message['role'], avatar=avatar):
#         st.markdown(message['content'])

# def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
#     """Yield chat response content from the Groq API response"""
#     for chunk in chat_completion:
#         if chunk.choices[0].delta.content:
#             yield chunk.choices[0].delta.content
    
# # Groq LLM Configuration
# def load_groq_llm():
#     return ChatGroq(model_option)

# # File Upload
# uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

# if uploaded_file is not None:
#     data = pd.read_csv(uploaded_file)
#     llm = load_groq_llm()
#     df = SmartDataframe(data, config={'llm': llm})

# # Chat Interactions
# if prompt := st.chat_input("Enter your prompt here..."):
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     with st.chat_message("user", avatar='👨‍💻'):
#         st.markdown(prompt)

#     # Fetch response from Groq API
#     try:
#         chat_completion = client.chat.completions.create(
#             model=model_option,
#             messages=[
#                 {
#                     "role": m["role"],
#                     "content": m["content"]
#                 }
#                 for m in st.session_state.messages
#             ],
#             max_tokens=max_tokens,
#             stream=True
#         )

#         # Use the generator function with st.write_stream
#         with st.chat_message("assistant", avatar="🤖"):
#             chat_responses_generator = generate_chat_responses(chat_completion)
#             full_response = st.write_stream(chat_responses_generator)
#     except Exception as e:
#         st.error(e, icon="🚨")

#     # Append the full response to session_state.messages
#     if isinstance(full_response, str):
#         st.session_state.messages.append(
#             {"role": "assistant", "content": full_response})
#     else:
#         # Handle the case where full_response is not a string
#         combined_response = "\n".join(str(item) for item in full_response)
#         st.session_state.messages.append(
#             {"role": "assistant", "content": combined_response})