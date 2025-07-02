#!/bin/bash
mkdir -p wordcloud-app/{pages,data/archive,components,.streamlit,assets}
touch wordcloud-app/data/.gitkeep wordcloud-app/data/archive/.gitkeep

# Requirements
cat <<EOF > wordcloud-app/requirements.txt
streamlit
pandas
wordcloud
matplotlib
pillow
qrcode
EOF

# .gitignore
cat <<EOF > wordcloud-app/.gitignore
__pycache__/
*.pyc
*.ttf
*.png
*.jpg
.DS_Store
.env
.venv/
data/*.csv
data/archive/
!data/.gitkeep
!data/archive/.gitkeep
EOF

# config.toml
cat <<EOF > wordcloud-app/.streamlit/config.toml
[theme]
primaryColor = "#4B8BBE"
backgroundColor = "#F5F7FA"
secondaryBackgroundColor = "#E0E0E0"
textColor = "#262730"
font = "sans serif"

[client]
toolbarMode = "minimal"
showErrorDetails = false
EOF

# Minimal submit.py
cat <<EOF > wordcloud-app/submit.py
import streamlit as st
st.title("Wordcloud Submission")
st.write("This is a placeholder.")
EOF

# Manage Sessions (admin)
cat <<EOF > "wordcloud-app/pages/Manage Sessions.py"
import streamlit as st
import os, json
from datetime import datetime

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.title("🔐 Admin Login")
    pwd = st.text_input("Enter admin password", type="password")
    if st.button("Login") and pwd == ADMIN_PASSWORD:
        st.session_state.admin_authenticated = True
        st.experimental_rerun()
    elif st.button("Login"):
        st.error("🚫 Incorrect password")
    st.stop()

st.title("🛠️ Manage Sessions")
st.sidebar.info("🛠️ Admin page loaded")

session_path = "data/sessions.json"
def load_sessions():
    if os.path.exists(session_path):
        with open(session_path, "r") as f:
            return json.load(f)
    return []

def save_sessions(sessions):
    with open(session_path, "w") as f:
        json.dump(sessions, f, indent=2)

sessions = load_sessions()

with st.expander("➕ Create New Session"):
    name = st.text_input("Session Name").strip().lower().replace(" ", "_")
    active = st.toggle("Active", True)
    col1, col2 = st.columns(2)
    start_time = col1.datetime_input("Start", datetime.now())
    end_time = col2.datetime_input("End", datetime.now())
    if st.button("Save Session") and name:
        sessions.append({
            "name": name,
            "active": active,
            "start": start_time.strftime("%Y-%m-%d %H:%M"),
            "end": end_time.strftime("%Y-%m-%d %H:%M")
        })
        save_sessions(sessions)
        st.success(f"Saved: {name}")
        st.experimental_rerun()

if sessions:
    st.subheader("📋 Sessions")
    for i, s in enumerate(sessions):
        with st.expander(f"🔹 {s['name']}"):
            s["active"] = st.toggle("Active", s["active"], key=f"a_{i}")
            s["start"] = st.text_input("Start", s["start"], key=f"s_{i}")
            s["end"] = st.text_input("End", s["end"], key=f"e_{i}")
    if st.button("💾 Save All"):
        save_sessions(sessions)
        st.success("✅ Sessions updated.")
EOF

# Sample sessions.json
cat <<EOF > wordcloud-app/data/sessions.json
[
  {
    "name": "demo_session",
    "active": true,
    "start": "2025-06-30 09:00",
    "end": "2025-07-02 18:00"
  }
]
EOF

# Zip it
zip -r wordcloud-app.zip wordcloud-app
echo "✅ Done: wordcloud-app.zip created!"
