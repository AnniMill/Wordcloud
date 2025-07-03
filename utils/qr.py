import qrcode
import streamlit as st
import io

def generate_qr_code(data: str):
    """Generate a QR code image from a string."""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def display_qr(session_name: str, session_url: str):
    """Render and download a QR code in Streamlit UI."""
    qr_img = generate_qr_code(session_url)
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)

    st.image(buf, caption=f"📲 QR Code for '{session_name}'", use_column_width=True)
    st.download_button(
        label="📥 Download QR Code",
        data=buf.getvalue(),
        file_name=f"{session_name}_qr.png",
        mime="image/png"
    )