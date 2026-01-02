import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(page_title="Al-Mu'allim VA", page_icon="🤖")
st.title("Al-Mu'allim VA (Free Version)")

# Secrets se API Key lena
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("API Key missing in Secrets!")
    st.stop()

# Chat history initialize karna
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani messages screen par dikhana
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if prompt := st.chat_input("Assalam-o-Alaikum! Main aap ki kya madad kar sakta hoon?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Model ka naam tabdeel kiya gaya hai taake error na aaye
            response = client.chat.completions.create(
                model="llama3-8b-8192", 
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
        except Exception as e:
            st.error(f"Error: {e}")
          
