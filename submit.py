import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import qrcode
from io import BytesIO

st.set_page_config(page_title="Submit a Response", page_icon="📝")
st.sidebar.info("🧪 Debug: This sidebar is rendering from submit.py")
st.title("💬 Word Cloud Submission Form")

# 🔐 Load valid sessions
session_file = "data/sessions.json"
now = datetime.now()

if os.path.exists(session_file):
    with open(session_file, "r") as f:
        all_sessions = json.load(f)
else:
    all_sessions = []

# ⏱️ Filter approved sessions by active status & time range
valid_sessions = [
    s["name"] for s in all_sessions
    if s.get("active")
    and datetime.strptime(s["start"], "%Y-%m-%d %H:%M") <= now <= datetime.strptime(s["end"], "%Y-%m-%d %H:%M")
]

# ⛔ If no sessions are available
if not valid_sessions:
    st.error("⚠️ No active sessions are currently available. Please check back later or contact your host.")
    st.stop()

# 👥 Select session from dropdown
session = st.selectbox("📛 Select Your Session", valid_sessions)

# 📝 Submission form
with st.form("submit_form"):
    response1 = st.text_input("Enter a word or phrase that describes your experience:")
    response2 = st.text_input("Enter another word or phrase:")
    submit = st.form_submit_button("Submit")

# ✅ Save submission
if submit:
    if not response1 and not response2:
        st.warning("Please enter at least one word or phrase.")
    else:
        df = pd.DataFrame([{
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "response1": response1,
            "response2": response2
        }])

        # Ensure folder exists
        file_path = f"data/submissions_{session}.csv"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Append or create file
        if os.path.exists(file_path):
            df.to_csv(file_path, mode="a", header=False, index=False)
        else:
            df.to_csv(file_path, index=False)

        st.success("✅ Your responses have been submitted!")

        # 🎁 Optional: Show QR code to resubmit
        st.markdown("---")
        st.markdown("🔁 Want to submit again or share this page?")
        qr = qrcode.make("https://wordcloud-n0u2.onrender.com")
        buf = BytesIO()
        qr.save(buf)
        st.image(buf.getvalue(), width=150, caption="Scan to reopen form")

        # 🔒 Optional: Admin link
        st.markdown(
            "<p style='text-align:center;'>Are you an <b>event host</b>? "
            "<a href='?page=Manage+Sessions'>Go to Manage Sessions 🔐</a></p>",
            unsafe_allow_html=True
        )
