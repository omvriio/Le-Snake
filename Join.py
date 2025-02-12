import streamlit as st
import asyncio
import websockets
import json

st.title("Join the Moroccan-Themed Snake Game")

# Extract the game ID from the URL query parameters
game_id = st.experimental_get_query_params().get("game_id", [""])[0]

if game_id:
    st.write(f"**You've joined the game with Game ID:** `{game_id}`")

    # Connect to WebSocket server and display the real-time game state
    async def receive_game_state():
        try:
            async with websockets.connect("ws://localhost:8000") as websocket:
                while True:
                    game_state = await websocket.recv()
                    state = json.loads(game_state)
                    st.write(f"**Game State:** {state}")
        except Exception as e:
            st.error(f"Failed to connect to game server: {e}")

    # Run the WebSocket client
    asyncio.run(receive_game_state())
else:
    st.write("No game ID provided. Please scan the QR code or enter a valid game ID.")

