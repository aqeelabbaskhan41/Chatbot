import json
import os
import streamlit as st
from groq import Groq

# Streamlit app setup
st.set_page_config(
    page_title="Apun ka Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Load the API key from package.json
working_dir = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(working_dir, "package.json")) as f:
        config_data = json.load(f)
    GROQ_API_KEY = config_data["GROQ_API_KEY"]
except (FileNotFoundError, json.JSONDecodeError):
    st.error("Failed to load API key from package.json")
    st.stop()

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

import streamlit as st

# Center the title
st.markdown("<h1 style='text-align: center;'>LLAMA 3.3-70 B</h1>", unsafe_allow_html=True)

# Display previous messages
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("Ask anything from LLAMA...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": "You are helpful"},
        *st.session_state.chat_history
    ]

    # API call
    resource = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    # ✅ Correct way to access the response
    assistant_response = resource.choices[0].message.content

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
