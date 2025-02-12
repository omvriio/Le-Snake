import streamlit as st
import uuid
import qrcode
from io import BytesIO
import streamlit.components.v1 as components
import random

# Function to generate a unique game session ID
def generate_game_id():
    return str(uuid.uuid4())

# Function to generate a QR code for the game session
def generate_qr_code(game_id):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"http://le-snake.streamlit.app/join?game_id={game_id}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf)
    byte_img = buf.getvalue()
    return byte_img

# Initialize session state
if 'game_id' not in st.session_state:
    st.session_state.game_id = generate_game_id()

# Streamlit app
st.title("Moroccan-Themed Co-op Snake Game")

# Display the game session ID
st.write("Your Game ID:", st.session_state.game_id)

# Generate and display a QR code for the game session
st.write("Scan this QR code to join the game:")
st.image(generate_qr_code(st.session_state.game_id))

# Input field to join a game
join_game_id = st.text_input("Enter Game ID to join:")
if join_game_id:
    st.session_state.game_id = join_game_id
    st.write("Joined game:", join_game_id)
    st.redirect("http://le-snake.streamlit.app/join?game_id={game_id}")
