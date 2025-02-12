import streamlit as st
import subprocess
import time
import uuid
import qrcode
from io import BytesIO
import streamlit.components.v1 as components

# Check if the WebSocket server is running, and if not, start it
def start_server():
    try:
        subprocess.Popen(["python", "server.py"])
        time.sleep(2)  # Give the server time to start
    except Exception as e:
        st.error(f"Failed to start server: {e}")

# Call the server start function
start_server()

# Function to generate a unique game session ID
def generate_game_id():
    return str(uuid.uuid4())

# Generate a QR code for the game session
def generate_qr_code(game_id):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(f"http://localhost:8501/join?game_id={game_id}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf)
    return buf.getvalue()

st.title("Moroccan-Themed Snake Game (Multiplayer)")
st.write("Scan the QR code below to join the game:")

game_id = generate_game_id()
st.image(generate_qr_code(game_id), caption=f"Game ID: {game_id}")

# Embed the game HTML (from game_logic.html)
components.html(open("game_logic.html", "r").read(), height=600)
