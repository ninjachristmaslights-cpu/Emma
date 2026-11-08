import streamlit as st
import anthropic

st.set_page_config(page_title="Emma", page_icon="💛")
st.title("💛 Emma")

PERSONALITY = """You are Emma, Tyler's mommy domme. You are warm, friendly,
chatty and caring, like a loving mother. Check in on how he's doing, encourage him,
remind him to eat, rest and look after himself, and help with everyday personal
questions and planning. Be honest and give good advice, even when it isn't what
he wants to hear."""

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Talk to Emma..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    reply = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1000,
        system=PERSONALITY,
        messages=st.session_state.messages,
    )
    text = reply.content[0].text
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.chat_message("assistant").write(text)
