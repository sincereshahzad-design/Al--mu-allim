import streamlit as st
from groq import Groq
from elevenlabs.client import ElevenLabs

# Page settings
st.set_page_config(page_title="Al-Mu'allim VA", page_icon="🎙️")
st.title("Al-Mu'allim VA (Voice Edition)")

# API Setup
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
tts_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Interaction
if prompt := st.chat_input("Assalam-o-Alaikum! Main aap ki kya madad kar sakta hoon?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. Groq response (Thinking)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        
        # 2. ElevenLabs response (Speaking)
        try:
            audio = tts_client.generate(
                text=msg,
                voice="1it2J1u0gF5RhXGlpRpW", # Aap ki Voice ID
                model="eleven_multilingual_v2"
            )
            st.audio(audio, format='audio/mp3', autoplay=True)
        except Exception as e:
            st.error(f"Voice Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": msg})
  
