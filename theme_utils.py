import streamlit as st
import json
import os
import shutil
from datetime import datetime

DEFAULT_THEME = {
    "backgroundColor": "#FFFFFF",
    "colormap": "viridis",
    "maxWords": 100,
    "randomSeed": 42
}

def init_theme():
    if "theme_settings" not in st.session_state:
        st.session_state.theme_settings = DEFAULT_THEME.copy()

def load_theme_from_file(uploaded_file):
    try:
        theme = json.load(uploaded_file)
        st.session_state.theme_settings.update(theme)
        return True, "✅ Theme loaded successfully!"
    except Exception as e:
        return False, f"⚠️ Error loading theme: {e}"

def export_theme_to_json(bg, colormap, max_words, seed):
    return json.dumps({
        "backgroundColor": bg,
        "colormap": colormap,
        "maxWords": max_words,
        "randomSeed": seed
    }, indent=2)

def archive_session_file(file_path):
    archive_dir = os.path.join("data", "archive")
    os.makedirs(archive_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.basename(file_path)
    archived = os.path.join(archive_dir, f"{timestamp}_{filename}")
    shutil.move(file_path, archived)
    return archived
