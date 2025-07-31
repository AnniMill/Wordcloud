# utils/sidebar.py

import streamlit as st

def render_sidebar(session_info=None):
    st.sidebar.title("Navigation")
    menu_choice = st.sidebar.radio("Go to:", ["Submit Response", "View Word Cloud", "Admin Panel"])

    # Optional session info block
    if session_info:
        st.sidebar.markdown("### Session Info")
        st.sidebar.text(f"Session: {session_info.get('name', 'N/A')}")
        st.sidebar.text(f"Start: {session_info.get('start', 'N/A')}")
        st.sidebar.text(f"End: {session_info.get('end', 'N/A')}")

    return menu_choice
