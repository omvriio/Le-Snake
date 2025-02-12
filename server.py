import asyncio
import websockets
import json

connected_clients = set()
game_state = {
    "player1": {"x": 9, "y": 10, "score": 0, "direction": "RIGHT"},
    "player2": {"x": 10, "y": 10, "score": 0, "direction": "LEFT"},
    "food": {"x": 5, "y": 5}
}

async def handler(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            player = data["player"]
            game_state[player] = data

            # Broadcast the updated game state to all connected clients
            await asyncio.wait([client.send(json.dumps(game_state)) for client in connected_clients])
    except websockets.ConnectionClosed:
        connected_clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8000):
        print("WebSocket server started on ws://0.0.0.0:8000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
