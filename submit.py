# ... [same imports as before]

# Add session input
session = st.text_input("📛 Session Name (e.g. team1, day2)", max_chars=30).strip().lower().replace(" ", "_")

if session:
    file_path = f"submissions_{session}.csv"

    with st.form("submission_form"):
        r1 = st.text_input("1️⃣ Response 1", max_chars=50)
        r2 = st.text_input("2️⃣ Response 2", max_chars=50)
        submitted = st.form_submit_button("🚀 Submit", use_container_width=True)

    if submitted:
        if r1.strip() and r2.strip():
            new_row = pd.DataFrame([{
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "response1": r1.strip(),
                "response2": r2.strip()
            }])

            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                df = pd.concat([df, new_row], ignore_index=True)
            else:
                df = new_row

            df.to_csv(file_path, index=False)
            st.session_state.submitted = True
            st.rerun()
        else:
            st.error("⚠️ Please fill in both responses.")
else:
    st.warning("Please enter a session name to begin.")
