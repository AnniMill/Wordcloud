import streamlit as st
import os, json
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import qrcode

# 🔐 Admin password
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password")

# Auth state
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if not st.session_state.admin_authenticated:
    st.title("🔐 Admin Login")
    pwd = st.text_input("Enter admin password", type="password")
    if st.button("Login") and pwd == ADMIN_PASSWORD:
        st.session_state.admin_authenticated = True
        st.rerun()
    elif st.button("Login", key="admin_login_fail"):
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

def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

sessions = load_sessions()

# ➕ Create session form
with st.expander("➕ Create New Session"):
    with st.form("create_session_form", clear_on_submit=False):
        name = st.text_input("📝 Session Name").strip().lower().replace(" ", "_")

        st.markdown("#### ⏱️ Start Time")
        col1a, col1b = st.columns(2)
        with col1a:
            start_date = st.date_input("📅 Date", key="start_date")
        with col1b:
            start_time = st.time_input("⏰ Time", key="start_time")

        st.markdown("#### ⏳ End Time")
        col2a, col2b = st.columns(2)
        with col2a:
            end_date = st.date_input("📅 Date", key="end_date")
        with col2b:
            end_time = st.time_input("⏰ Time", key="end_time")

        active = st.toggle("✅ Active", value=True)
        submitted = st.form_submit_button("💾 Save Session")

        if submitted:
            start_dt = datetime.combine(start_date, start_time)
            end_dt = datetime.combine(end_date, end_time)
            existing_names = [s["name"] for s in sessions]

            if not name:
                st.warning("⚠️ Please enter a session name.")
            elif name in existing_names:
                st.warning(f"⚠️ Session '{name}' already exists.")
            elif start_dt >= end_dt:
                st.warning("⚠️ Start time must be before end time.")
            else:
                sessions.append({
                    "name": name,
                    "active": active,
                    "start": start_dt.strftime("%Y-%m-%d %H:%M"),
                    "end": end_dt.strftime("%Y-%m-%d %H:%M")
                })
                save_sessions(sessions)
                st.success(f"✅ Session '{name}' created.")
                st.rerun()

# 📋 View + edit sessions
if sessions:
    st.subheader("📄 Existing Sessions")
    for i, s in enumerate(sessions):
        with st.expander(f"🔹 {s['name']}"):
            s["active"] = st.toggle("Active", value=s["active"], key=f"active_{i}")
            s["start"] = st.text_input("Start Time", value=s["start"], key=f"start_{i}")
            s["end"] = st.text_input("End Time", value=s["end"], key=f"end_{i}")

            # 🧠 Word Cloud Preview
            st.markdown("---")
            st.write("🧠 Word Cloud Preview")

            file_path = f"data/submissions_{s['name']}.csv"
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                words = " ".join(df["response1"].fillna("").tolist() + df["response2"].fillna("").tolist())

                if words.strip():
                    mask_path = "assets/star_mask.png"
                    mask = np.array(Image.open(mask_path)) if os.path.exists(mask_path) else None

                    font_path = "assets/PlayfairDisplay.ttf" if os.path.exists(font_path := "assets/PlayfairDisplay.ttf") else None

                    cmap = st.selectbox("🎨 Colormap", ["viridis", "plasma", "twilight", "cividis", "magma"], key=f"cmap_{i}")

                    wc = WordCloud(width=800, height=400, background_color="white", font_path=font_path, mask=mask, colormap=cmap).generate(words)

                    fig, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wc, interpolation="bilinear")
                    ax.axis("off")
                    st.pyplot(fig)

                    buf_wc = io.BytesIO()
                    wc.to_image().save(buf_wc, format="PNG")
                    st.download_button("📥 Download Word Cloud", buf_wc.getvalue(), file_name=f"{s['name']}_wordcloud.png", mime="image/png", key=f"download_wc_{i}")
                else:
                    st.info("No responses yet to render a word cloud.")
            else:
                st.info("🗂️ No submission file found.")

            # 📤 Share Session Popover
            with st.popover("📤 Share Session", use_container_width=True):
                session_url = f"https://wordcloud-n0u2.onrender.com/?session={s['name']}"
                st.write("Scan or copy the link below to share this session.")
                st.code(session_url, language="text")
                qr_img = generate_qr_code(session_url)
                buf_qr = io.BytesIO()
                qr_img.save(buf_qr, format="PNG")
                st.image(qr_img, caption="📲 QR Code", use_column_width=True)
                st.download_button("📥 Download QR Code", buf_qr.getvalue(), file_name=f"{s['name']}_qr.png", mime="image/png",key=f"download_qr_{i}")

    if st.button("💾 Save All Changes", key-"save_all_sessions"):
        save_sessions(sessions)
        st.success("✅ Sessions updated.")
else:
    st.info("No sessions found. Add one above to get started.")
