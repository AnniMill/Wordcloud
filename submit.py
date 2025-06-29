import streamlit as st
import pandas as pd
from datetime import datetime
import os
import qrcode
from io import BytesIO
from PIL import Image

APP_URL = "https://wordcloud-n0u2.onrender.com"

st.set_page_config(page_title="🌟 Wordcloud Submission", page_icon="📝", layout="centered")

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.session_state.submitted:
    st.markdown("## 🙌 Thanks for contributing!")
    st.success("Your words have been saved to the word cloud.")
    st.balloons()

    qr = qrcode.make(APP_URL)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    st.image(Image.open(buf), caption="Scan to submit again", use_container_width=True)
    st.markdown(f"[🔁 Submit again]({APP_URL})")
    st.stop()

st.markdown("""
    <div style='text-align: center;'>
        <h2 style='color: #4B8BBE;'>✨ Share Your Voice ✨</h2>
        <p>Choose your session and add two words to shape the cloud.</p>
    </div>
""", unsafe_allow_html=True)

session = st.text_input("📛 Session Name (e.g. team1, day2)", max_chars=30).strip().lower().replace(" ", "_")

if session:
    file_path = f"data/submissions_{session}.csv"

    with st.form("submission_form"):
        r1 = st.text_input("1️⃣ Response 1", max_chars=50)
        r2 = st.text_input("2️⃣ Response 2", max_chars=50)
        submitted = st.form_submit_button("🚀 Submit", use_container_width=True)

    if submitted:
        if r1.strip() and r2.strip():
            new_row = pd.DataFrame([{
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "response1": r1.strip(),
                "response2": r2.strip()
            }])

            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df = pd.concat([df, new_row], ignore_index=True)
            else:
                df = new_row
st.markdown("---")
st.markdown(
    "<p style='text-align:center;'>Are you an <b>event host</b>? "
    "<a href='?page=Manage+Sessions'>Go to Manage Sessions 🔒</a></p>",
    unsafe_allow_html=True
)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            df.to_csv(file_path, index=False)
            st.session_state.submitted = True
            st.rerun()
        else:
            st.error("⚠️ Please fill in both responses.")
else:
    st.info("Enter a session name to begin.")
