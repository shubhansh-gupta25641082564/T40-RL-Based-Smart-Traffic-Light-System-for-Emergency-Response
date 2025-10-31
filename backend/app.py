from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json

app = FastAPI(title="Traffic Control Dashboard API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global simulation state
simulation_state = {
    "is_running": False,
    "current_step": 0,
    "metrics": {
        "total_vehicles": 0,
        "waiting_time": 0,
        "emergency_events": 0,
        "phase": "NS",
    }
}

@app.get("/")
async def root():
    return {"message": "Traffic Control API", "status": "online"}

@app.get("/api/status")
async def get_status():
    return simulation_state

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send simulation state every second
            await websocket.send_json(simulation_state)
            await asyncio.sleep(1)
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)