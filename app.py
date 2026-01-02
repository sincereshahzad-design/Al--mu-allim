import streamlit as st
from groq import Groq
from elevenlabs.client import ElevenLabs

# Page Config
st.set_page_config(page_title="Al-Mu'allim VA", page_icon="🎙️")
st.title("Al-Mu'allim VA (Voice Edition)")

# Initialize Clients using Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
tts_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Assalam-o-Alaikum! Main aap ki kya madad kar sakta hoon?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # 1. Get Text Response from Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        
        # 2. Get Voice Response from ElevenLabs (Updated Method)
        try:
            audio_generator = tts_client.text_to_speech.convert(
                voice_id="1it2J1u0gF5RhXGlpRpW", # Your Voice ID
                text=msg,
                model_id="eleven_multilingual_v2"
            )
            
            # Convert generator to bytes for st.audio
            audio_data = b"".join(list(audio_generator))
            st.audio(audio_data, format='audio/mp3', autoplay=True)
            
        except Exception as e:
            st.error(f"Voice Error: {e}")
            
    st.session_state.messages.append({"role": "assistant", "content": msg})
  
