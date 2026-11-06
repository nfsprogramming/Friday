import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from livekit import api

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Generate LiveKit Token
@app.get("/api/token")
async def get_token():
    url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")

    if not url or not api_key or not api_secret:
        raise HTTPException(status_code=500, detail="Missing LiveKit credentials in .env")

    # Generate a participant token for the default room (assuming "my-room")
    # You can change the room name or make it dynamic if needed
    room_name = "friday-room" 
    participant_name = "User"

    token = api.AccessToken(api_key, api_secret)\
        .with_identity(participant_name)\
        .with_name(participant_name)\
        .with_grants(api.VideoGrant(room_join=True, room=room_name))

    return {
        "serverUrl": url,
        "token": token.to_jwt()
    }

# Serve the Vite built frontend
dist_path = os.path.join(os.path.dirname(__file__), "frontend", "dist")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("ui_server:app", host="127.0.0.1", port=8080, reload=True)
