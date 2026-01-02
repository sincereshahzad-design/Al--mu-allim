import streamlit as st
from groq import Groq
from elevenlabs.client import ElevenLabs
from streamlit_mic_recorder import mic_recorder

# Page Setup
st.set_page_config(page_title="Al-Mu'allim VA", page_icon="🎙️")
st.title("Al-Mu'allim VA (Voice & Mike)")

# API Setup
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    tts_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])
except Exception as e:
    st.error("Secrets missing! Check GROQ_API_KEY and ELEVENLABS_API_KEY in Settings.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MIKE / VOICE INPUT SECTION ---
st.write("---")
st.write("Record your voice:")
audio_input = mic_recorder(start_prompt="🔴 Start Recording", stop_prompt="⏹️ Stop & Send", key='recorder')

user_text = st.chat_input("Or type here...")

# If voice is recorded
if audio_input:
    # Note: For actual speech-to-text, you'd need Groq's Whisper model here.
    # Currently, this placeholder detects that you spoke.
    user_text = "Mera audio message suniye." 

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        # 1. Text Response
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        
        # 2. Voice Output
        try:
            audio_gen = tts_client.text_to_speech.convert(
                voice_id="1it2J1u0gF5RhXGlpRpW",
                text=msg,
                model_id="eleven_multilingual_v2"
            )
            audio_data = b"".join(list(audio_gen))
            st.audio(audio_data, format='audio/mp3', autoplay=True)
        except Exception as e:
            st.error(f"Voice Error (Check API Key): {e}")

    st.session_state.messages.append({"role": "assistant", "content": msg})
      
