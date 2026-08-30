"""
Voice Agent Demo
-----------------
A small end-to-end voice pipeline: record your voice in the browser,
transcribe it to text, send it to Gemini for a reply, and hear the
reply spoken back to you.

Pipeline: microphone → speech-to-text → LLM → text-to-speech → playback
"""

import io
import os

import speech_recognition as sr
import streamlit as st
import google.generativeai as genai
from gtts import gTTS

st.set_page_config(page_title="Voice Agent Demo", page_icon="🎙️", layout="centered")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_model():
    """Build a Gemini model from an API key in env var or sidebar input."""
    api_key = os.environ.get("GOOGLE_API_KEY") or st.session_state.get("api_key")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-3.6-flash")


def transcribe_audio(audio_bytes: bytes) -> str:
    """Convert recorded WAV audio bytes into text using free speech recognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data)


def get_ai_reply(model, user_text: str) -> str:
    """Send the transcribed text to Gemini and return a short spoken-style reply."""
    prompt = f"""
You are a friendly, helpful voice assistant. Someone just said this to
you out loud: "{user_text}"

Reply conversationally in 1-3 short sentences, the way you'd actually
speak out loud — no bullet points, no markdown formatting, since this
reply will be converted to speech.
"""
    response = model.generate_content(prompt, generation_config={"temperature": 0.6})
    return response.text.strip()


def text_to_speech(text: str) -> bytes:
    """Convert text into spoken audio (MP3 bytes) using free Google TTS."""
    tts = gTTS(text=text, lang="en")
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return buffer.read()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

st.sidebar.header("Settings")

if not os.environ.get("GOOGLE_API_KEY"):
    st.session_state.api_key = st.sidebar.text_input(
        "Google Gemini API key", type="password",
        help="Get a free one at aistudio.google.com. Not saved anywhere, only used for this session.",
    )
else:
    st.sidebar.success("API key loaded from environment.")

st.sidebar.markdown("---")
st.sidebar.caption(
    "Speech-to-text and text-to-speech both use free Google services "
    "and need no extra API key — only Gemini needs one."
)

# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------

st.title("🎙️ Voice Agent Demo")
st.caption("Speak → AI transcribes it → AI replies → hear the reply spoken back")

st.markdown("### 1. Record your message")
audio_value = st.audio_input("Click the mic and speak")

if audio_value is not None:
    model = get_model()
    if model is None:
        st.error("Please enter your Google Gemini API key in the sidebar first.")
    else:
        with st.spinner("Transcribing your voice..."):
            try:
                audio_bytes = audio_value.getvalue()
                transcript = transcribe_audio(audio_bytes)
            except sr.UnknownValueError:
                transcript = None
                st.error(
                    "Couldn't understand the audio — try speaking a bit "
                    "louder or closer to the mic, then record again."
                )
            except Exception as exc:  # noqa: BLE001
                transcript = None
                st.error(f"Transcription failed: {exc}")

        if transcript:
            st.markdown("### 2. What you said")
            st.info(transcript)

            with st.spinner("Getting a reply..."):
                try:
                    reply_text = get_ai_reply(model, transcript)
                except Exception as exc:  # noqa: BLE001
                    reply_text = None
                    st.error(f"Something went wrong getting a reply: {exc}")

            if reply_text:
                st.markdown("### 3. AI's reply")
                st.success(reply_text)

                with st.spinner("Converting reply to speech..."):
                    try:
                        speech_bytes = text_to_speech(reply_text)
                        st.markdown("### 4. Listen to the reply")
                        st.audio(speech_bytes, format="audio/mp3")
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Text-to-speech failed: {exc}")
