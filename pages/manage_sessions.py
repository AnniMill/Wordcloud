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

# ➕ Create session
with st.expander("➕ Create New Session"):
    name = st.text_input("Session Name")
