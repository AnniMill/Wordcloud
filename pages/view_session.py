import streamlit as st
import pandas as pd
import json
import os
from utils.wordclouds import generate_words, render_wordcloud, get_mask, get_font
from datetime import datetime

st.set_page_config(page_title="Session View", layout="wide")

# 🔎 Get session name from query parameter
session_name = st.query_params.get("session")
if not session_name:
    st.error("No session specified in URL.")
    st.stop()

# 📖 Load session metadata
def get_session_data(name):
    if not os.path.exists("data/sessions.json"):
        return None
    with open("data/sessions.json", "r") as f:
        sessions = json.load(f)
        for s in sessions:
            if s["name"] == name:
                return s
    return None

session = get_session_data(session_name)
if not session:
    st.error(f"No matching session found: '{session_name}'")
    st.stop()

# 💬 Show session question/title
st.title("📘 Session")
if session.get("question"):
    st.subheader(session["question"])
else:
    st.subheader(session["name"])

# ⏳ Show status
try:
    start = datetime.strptime(session["start"], "%Y-%m-%d %H:%M")
    end = datetime.strptime(session["end"], "%Y-%m-%d %H:%M")
    now = datetime.now()
    if now < start:
        st.info(f"⏳ Starts in: {str(start - now).split('.')[0]}")
    elif now > end:
        st.warning("🚫 This session has ended.")
    else:
        st.success("🟢 This session is currently active.")
except:
    pass

# 📂 Load submissions
data_path = f"data/submissions_{session_name}.csv"
if not os.path.exists(data_path):
    st.info("No responses found for this session.")
    st.stop()

df = pd.read_csv(data_path)
words = generate_words(df)

if words.strip():
    colormap = st.selectbox("🎨 Colormap", ["viridis", "plasma", "twilight", "cividis", "magma"])
    font = get_font()
    mask = get_mask()
    fig, buf_wc = render_wordcloud(words, font_path=font, mask=mask, colormap=colormap)

    st.subheader("🧠 Word Cloud")
    st.pyplot(fig)

    st.download_button(
        "📥 Download Word Cloud",
        data=buf_wc.getvalue(),
        file_name=f"{session_name}_wordcloud.png",
        mime="image/png"
    )
else:
    st.info("Not enough content to generate a word cloud.")
