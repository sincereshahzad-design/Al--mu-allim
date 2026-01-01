import streamlit as st
from openai import OpenAI

# 1. Setup the Page Theme (Emerald & Gold)
st.set_page_config(page_title="Al-Mu'allim VA", page_icon="🌙")
st.markdown("""
    <style>
    .stApp { background-color: #004d40; color: white; }
    .stTextInput > div > div > input { background-color: #f0f4f1; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌙 Al-Mu'allim (The Teacher)")
st.subheader("Your Private & Secure AI for Islamic Guidance")

# 2. Connection to AI
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. User Input
if prompt := st.chat_input("Ask your question privately..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Logic
    with st.chat_message("assistant"):
        system_msg = "You are Al-Mu’allim, a kind Islamic teacher. Use Quran/Hadith. Be non-judgmental for shy users."
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_msg}] + st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
      
