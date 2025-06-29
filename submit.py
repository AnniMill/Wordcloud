# submit.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import qrcode
from io import BytesIO
from PIL import Image

APP_URL = "https://your-app-url.onrender.com"

st.set_page_config(page_title="Wordcloud Submission", layout="centered")

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

if st.session_state.submitted:
    st.markdown("## 🙏 Thanks for sharing!")
    st.success("Your words have been added to the wordcloud.")
    st.balloons()

    qr = qrcode.make(APP_URL)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    st.image(Image.open(buf), caption="Scan to share the link", use_column_width=False)
    st.markdown(f"[Or click here to resubmit]({APP_URL})")
    st.stop()

st.title("🎤 Submit Your Responses")
st.markdown("Enter two meaningful words or short phrases:")

with st.form("submission_form"):
    r1 = st.text_input("Response 1 (max 50 chars)", max_chars=50)
    r2 = st.text_input("Response 2 (max 50 chars)", max_chars=50)
    submitted = st.form_submit_button("Submit 🚀")

if submitted and r1 and r2:
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "response1": r1.strip(),
        "response2": r2.strip()
    }

    file_path = "submissions.csv"
    df = pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(file_path, index=False)

    st.session_state.submitted = True
    st.rerun()
