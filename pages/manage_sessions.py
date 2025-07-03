import streamlit as st
import os, json
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# 🔐 Admin password
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme")

# Auth state
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

# ✅ Logged in
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

# ➕ Create session form
with st.expander("➕ Create New Session"):
    with st.form("create_session_form", clear_on_submit=False):
        name = st.text_input("📝 Session Name").strip().lower().replace(" ", "_")
        col1, col2 = st.columns(2)
        with col1:
            start_time = st.datetime_input("⏱️ Start Time", value=datetime.now())
        with col2:
            end_time = st.datetime_input("⏳ End Time", value=datetime.now())

        active = st.toggle("✅ Active", value=True)
        submitted = st.form_submit_button("💾 Save Session")

        if submitted:
            # Validate name
            existing_names = [s["name"] for s in sessions]
            if not name:
                st.warning("⚠️ Please enter a session name.")
            elif name in existing_names:
                st.warning(f"⚠️ A session named '{name}' already exists.")
            elif start_time >= end_time:
                st.warning("⚠️ Start time must be before end time.")
            else:
                sessions.append({
                    "name": name,
                    "active": active,
                    "start": start_time.strftime("%Y-%m-%d %H:%M"),
                    "end": end_time.strftime("%Y-%m-%d %H:%M")
                })
                save_sessions(sessions)
                st.success(f"✅ Session '{name}' created successfully!")
                st.experimental_rerun()
