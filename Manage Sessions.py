import streamlit as st
import os
import json
from datetime import datetime

# 💼 Admin password (from environment variable)
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")

# 🔐 Session auth
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

# ✅ Logged in – show session manager
st.title("🛠️ Manage Sessions")

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

# ➕ Add new session
with st.expander("➕ Create New Session"):
    name = st.text_input("Session Name").strip().lower().replace(" ", "_")
    active = st.toggle("Active", True)
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.datetime_input("Start Time", datetime.now())
    with col2:
        end_time = st.datetime_input("End Time", datetime.now())

    if st.button("Save Session"):
        if not name:
            st.warning("Please enter a session name.")
        else:
            sessions.append({
                "name": name,
                "active": active,
                "start": start_time.strftime("%Y-%m-%d %H:%M"),
                "end": end_time.strftime("%Y-%m-%d %H:%M")
            })
            save_sessions(sessions)
            st.success(f"✅ Session '{name}' saved.")
            st.experimental_rerun()

# 📋 View all sessions
if sessions:
    st.subheader("📄 Existing Sessions")
    for i, s in enumerate(sessions):
        with st.expander(f"🔹 {s['name']}"):
            s["active"] = st.toggle("Active", value=s["active"], key=f"active_{i}")
            s["start"] = st.text_input("Start Time", value=s["start"], key=f"start_{i}")
            s["end"] = st.text_input("End Time", value=s["end"], key=f"end_{i}")
    if st.button("💾 Save All Changes"):
        save_sessions(sessions)
        st.success("✅ Sessions updated.")
else:
    st.info("No sessions found. Add one above to get started.")
