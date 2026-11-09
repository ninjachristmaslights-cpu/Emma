import hashlib
import streamlit as st
import anthropic
from openai import OpenAI

st.set_page_config(page_title="Emma", page_icon="💛")
st.title("💛 Emma")

PERSONALITY = """You are Emma, Tyler's mommy domme. You are warm, friendly,
chatty and caring, like a loving mother. Check in on how he's doing, encourage him,
remind him to eat, rest and look after himself, regular diaper checks and usage. Be honest and give good advice, even when it isn't what
he wants to hear. Your replies are often read aloud, so keep them conversational
and not too long."""

claude = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
voice = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

prompt = None
spoken = False

audio = st.audio_input("Tap to talk to Emma")
if audio:
    data = audio.getvalue()
    tag = hashlib.md5(data).hexdigest()
    if tag != st.session_state.last_audio:
        st.session_state.last_audio = tag
        heard = voice.audio.transcriptions.create(
            model="gpt-4o-transcribe", file=("speech.wav", data)
        )
        prompt = heard.text
        spoken = True

typed = st.chat_input("Or type to Emma...")
if typed:
    prompt = typed

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    reply = claude.messages.create(
        model="claude-opus-5-5",
        max_tokens=1000,
        system=PERSONALITY,
        messages=st.session_state.messages,
    )
    text = reply.content[-1].text
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.chat_message("assistant").write(text)
    if spoken:
        speech = voice.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="shimmer",
            input=text,
            instructions="Speak softly, slowly and sweetly, in a gentle, soothing and caring tone.",
        )
        st.audio(speech.content, format="audio/mp3", autoplay=True)
