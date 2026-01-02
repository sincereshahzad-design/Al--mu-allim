import streamlit as st
from groq import Groq

# Page settings
st.set_page_config(page_title="Al-Mu'allim VA", page_icon="🤖")
st.title("Al-Mu'allim VA (Free)")

# Secrets سے Key اٹھانا
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Chat history initialize کرنا
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani messages dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handle کرنا
if prompt := st.chat_input("Puchiye jo aap puchna chahte hain..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Groq model ka istemal
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
  
