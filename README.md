# 🎙️ Voice Agent Demo

A small end-to-end voice pipeline: speak into your browser mic, have
your speech transcribed to text, get an AI-generated reply, and hear
that reply spoken back to you — all in the browser, no phone system or
call center software involved.

🔗 **Live demo:** (add your Streamlit Cloud link here once deployed)

## Why I built this

At my job, I build voice agent pipelines — scripting the flow of
turning speech into text, processing it, and turning a response back
into speech. This project is a small, from-scratch, public version of
that same underlying pattern: speech-to-text → LLM reasoning →
text-to-speech, built to demonstrate the concept end-to-end without
any proprietary company code or data.

## How it works

```
Microphone recording (browser)
        ↓
Speech-to-text (free Google recognition, via SpeechRecognition library)
        ↓
Gemini API — generates a short, conversational reply
        ↓
Text-to-speech (free Google TTS, via gTTS)
        ↓
Audio playback in the browser
```

## Tech stack

- **Python**
- **Streamlit** — browser mic recording (`st.audio_input`) and the
  overall app interface
- **SpeechRecognition** (using Google's free web speech API) —
  converts recorded audio into text, no separate API key needed
- **Google Gemini API** (`gemini-3.6-flash`) — generates the reply
- **gTTS** (Google Text-to-Speech) — converts the reply back into
  spoken audio, no separate API key needed

## Setup

1. Clone this repo and move into it:
   ```bash
   git clone <this-repo-url>
   cd voice-agent-demo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Get a free Google Gemini API key from https://aistudio.google.com
   (this is the only key this project needs — speech-to-text and
   text-to-speech are both free with no key required)

5. Set it as an environment variable:
   ```bash
   export GOOGLE_API_KEY="your-key-here"     # on Windows: set GOOGLE_API_KEY=your-key-here
   ```

## Running it

```bash
streamlit run app.py
```

Click the microphone button, speak, and wait a few seconds for the
transcript, reply, and spoken audio to appear.

## Known limitations

- The free speech recognition service works best with clear, quiet
  audio — background noise or heavy accents can reduce accuracy.
- Only supports English (`lang="en"`) for text-to-speech in this
  version.
- No conversation memory — each recording is treated as a fresh,
  standalone message.

## Possible next steps

- Add conversation history so the agent remembers earlier turns
- Support multiple languages for both transcription and speech output
- Swap in a paid, more accurate speech-to-text service (e.g. Whisper)
  for production-grade accuracy
