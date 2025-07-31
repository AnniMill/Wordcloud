import streamlit as st
import pandas as pd
import os, json
from datetime import datetime

st.set_page_config(page_title="Submit Your Response", layout="centered")

# 🔎 Get session name from URL
session_name = st.query_params.get("session")
if not session_name:
    st.error("No session specified.")
    st.stop()

# 📖 Load session data
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
    st.error(f"Session '{session_name}' not found.")
    st.stop()

# 🧭 Display sidebar info
start = datetime.strptime(session["start"], "%Y-%m-%d %H:%M")
end = datetime.strptime(session["end"], "%Y-%m-%d %H:%M")
now = datetime.now()

st.sidebar.markdown("### 📂 Session Info")
st.sidebar.write(f"**Session:** `{session_name}`")
st.sidebar.write(f"**Question:** {session.get('question', 'N/A')}")
st.sidebar.write(f"**Start:** {start.strftime('%Y-%m-%d %H:%M')}")
st.sidebar.write(f"**End:** {end.strftime('%Y-%m-%d %H:%M')}")
st.sidebar.write(f"**Current Time:** {now.strftime('%Y-%m-%d %H:%M')}")

# 🧭 Display session info
st.title("📝 Submit Your Response")
st.subheader(session.get("question", f"Session: {session_name}"))

if now < start:
    st.warning(f"⏳ This session hasn't started yet — starts in {str(start - now).split('.')[0]}.")
    st.stop()
elif now > end:
    st.error("🚫 This session has ended.")
    st.stop()

# 💬 Response Form
with st.form("response_form"):
    r1 = st.text_input("💡 First response (required)").strip()
    r2 = st.text_input("✨ Second response (optional)").strip()
    submitted = st.form_submit_button("📩 Submit")

    if submitted:
        if not r1:
            st.warning("Please enter at least one response.")
        else:
            file_path = f"data/submissions_{session_name}.csv"
            df_new = pd.DataFrame([{"response1": r1, "response2": r2}])
            if os.path.exists(file_path):
                df_existing = pd.read_csv(file_path)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_combined = df_new
            df_combined.to_csv(file_path, index=False)
            st.success("✅ Response submitted!")
