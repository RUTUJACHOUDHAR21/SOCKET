from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

app = FastAPI()

# Allow frontend from any origin (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (e.g., index.html)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def get():
    with open("index.html") as f:
        return HTMLResponse(f.read())

clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast the message to all clients
            for client in clients:
                if client != websocket:  # Send to other clients, not the sender
                    await client.send_text(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clients.remove(websocket)
