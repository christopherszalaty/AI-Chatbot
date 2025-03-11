import streamlit as st
import requests
import time

#FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat/"

# Streamlit interface configuration
st.set_page_config(page_title="Chris's ChatBot", page_icon="AI-icon.jpg", layout="wide")
st.markdown('<font size="2">© 2025 Created by Krzysztof Szalaty</font>', unsafe_allow_html=True)

col1, col2 = st.columns([5,1])
col1.markdown(" ### 💬 Chatbot AI")
col1.markdown("##### Ask me anything!")
st.write("")

#Setting model temperature
creativity = col2.slider("Adjust LLM model creativity", 0.0, 1.0, value = 0.3, step = 0.05)
col2.metric(label = "LLM Temperature", value = creativity)

#Selecting the LLM model
model_name = col2.selectbox(
    "Select LLM model",
    [
        "llama-3.3-70b-versatile", 
        "deepseek-r1-distill-llama-70b", 
        "llama-3.2-90b-vision-preview",
        "qwen-qwq-32b"
    ]
)

#Chat history initialization

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])
    
user_input = st.chat_input("Type your message...")

if user_input: 
    #Adding the user input to the chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    payload = {
        "message": user_input,
        "creativity": creativity,
        "model": model_name
    }
    #Sending the response to the backend
    with st.spinner("Thinking..."):
        response = requests.post(API_URL, json = payload)
        time.sleep(1)
        
    if response.status_code == 200:
        response_data = response.json()
        #Adding the AI response to the chat history
        ai_response = response_data.get("response", "No response received")
        st.session_state["messages"].append({"role": "assistant", "content": ai_response})
        st.write(ai_response)
    else:
        st.error(f"Error: {response.status_code}: {response.text}")
