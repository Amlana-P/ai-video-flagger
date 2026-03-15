from fastapi import FastAPI, UploadFile, File
import uuid
import shutil
import os

from frame_extractor import extract_frames
from detector import analyze_video
from cleanup import cleanup

UPLOAD_DIR = "uploads"

app = FastAPI()

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    video_id = str(uuid.uuid4())
    path = f"{UPLOAD_DIR}/{video_id}.mp4"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    frames = extract_frames(path)

    result = analyze_video(frames)

    cleanup()

    return result