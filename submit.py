# submit.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import qrcode
from io import BytesIO
from PIL import Image

# 🔗 Update this to match your deployed Render URL
APP_URL = "https://wordcloud-n0u2.onrender.com"

# 🔧 Config
st.set_page_config(page_title="🌟 Wordcloud Submission", page_icon="📝", layout="centered")

# 🧠 Session flag for thank-you logic
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# 🙏 Thank You page
if st.session_state.submitted:
    st.markdown("## 🙌 Thanks for contributing!")
    st.success("Your words have been saved to the word cloud.")
    st.balloons()

    # 🔲 QR Code
    qr = qrcode.make(APP_URL)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    img = Image.open(buf)
    st.image(img, caption="Scan to reopen this form", use_container_width=True)

    st.markdown(f"🔁 [Click here to submit again]({APP_URL})")
    st.stop()

# 📝 Main Submission Form
st.markdown("""
    <div style='text-align: center;'>
        <h2 style='color: #4B8BBE;'>✨ Share Your Voice ✨</h2>
        <p>Contribute two words or short phrases to shape the live word cloud below.</p>
    </div>
""", unsafe_allow_html=True)

with st.form("submission_form"):
    response1 = st.text_input("1️⃣ Response 1 (max 50 characters)", max_chars=50)
    response2 = st.text_input("2️⃣ Response 2 (max 50 characters)", max_chars=50)
    submitted = st.form_submit_button("🚀 Submit", use_container_width=True)

# 💾 Save responses
if submitted:
    if response1.strip() and response2.strip():
        new_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "response1": response1.strip(),
            "response2": response2.strip()
        }

        file_path = "submissions.csv"
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        else:
            df = pd.DataFrame([new_entry])

        df.to_csv(file_path, index=False)

        st.session_state.submitted = True
        st.rerun()
    else:
        st.error("⚠️ Both responses are required. Please fill in both fields.")
