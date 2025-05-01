import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            message_data = json.loads(message)
            sender = message_data.get("sender", "Anonymous")
            text = message_data.get("message", "")
            print(f"Received message from {sender}: {text}")
            # Broadcast the message to all connected clients
            for client in connected_clients:
                if client != websocket and client.open:
                    await client.send(json.dumps({"sender": sender, "message": text}))
    except websockets.ConnectionClosed:
        print("A client disconnected")
    finally:
        connected_clients.remove(websocket)

async def main():
    #  Use the host and port that Render provides.  For Render, you might need to use 10000
    async with websockets.serve(handler, host='0.0.0.0', port=10000): # Important for Render
        print("WebSocket server started at wss://0.0.0.0:10000")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
