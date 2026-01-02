import streamlit as st
from groq import Groq

# Page settings
st.set_page_config(page_title="Al-Mu'allim VA", page_icon="🤖")
st.title("Al-Mu'allim VA (Free)")

# Secrets se Groq Key uthana
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Chat history initialize karna
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani messages dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input handle karna
if prompt := st.chat_input("Puchiye jo aap puchna chahte hain..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Sahi model name yahan hai
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    
    st.session_state.messages.append({"role": "assistant", "content": msg})
  
