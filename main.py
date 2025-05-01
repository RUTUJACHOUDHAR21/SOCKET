from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            username = self.active_connections[websocket]
            del self.active_connections[websocket]
            return username

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

    def add_user(self, websocket: WebSocket, username: str):
        self.active_connections[websocket] = username

    def get_username(self, websocket: WebSocket):
        return self.active_connections.get(websocket, "Unknown")

manager = ConnectionManager()

@app.api_route("/", methods=["GET", "HEAD"])
async def get():
    with open("index.html") as f:
        return HTMLResponse(f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            now = datetime.utcnow().isoformat()

            if data["type"] == "join":
                manager.add_user(websocket, data["username"])
                await manager.broadcast({
                    "type": "system",
                    "text": f"{data['username']} joined the chat.",
                    "time": now
                })

            elif data["type"] == "leave":
                username = manager.disconnect(websocket)
                if username:
                    await manager.broadcast({
                        "type": "system",
                        "text": f"{username} left the chat.",
                        "time": now
                    })
                break

            elif data["type"] == "message":
                await manager.broadcast({
                    "type": "message",
                    "username": data["username"],
                    "text": data["text"],
                    "time": now
                })

    except WebSocketDisconnect:
        username = manager.disconnect(websocket)
        if username:
            await manager.broadcast({
                "type": "system",
                "text": f"{username} disconnected.",
                "time": datetime.utcnow().isoformat()
            })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000)
