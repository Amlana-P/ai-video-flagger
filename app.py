from fastapi import FastAPI, UploadFile
import shutil
import os
import subprocess
import uuid

from video_processor import extract_frames
from detector import analyze_frames

app = FastAPI()

UPLOAD_DIR = "uploads"
FRAME_DIR = "frames"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)


def extract_frames(video_path):

    os.makedirs(FRAME_DIR, exist_ok=True)

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", "fps=1",
        f"{FRAME_DIR}/frame_%04d.jpg"
    ]

    subprocess.run(command)

    frames = sorted(os.listdir(FRAME_DIR))

    return frames


def cleanup(video_path):

    if os.path.exists(video_path):
        os.remove(video_path)

    for f in os.listdir(FRAME_DIR):
        os.remove(os.path.join(FRAME_DIR, f))


@app.get("/")
def home():
    return {"status": "API running"}



app = FastAPI()

UPLOAD_DIR = "uploads"
FRAME_DIR = "frames"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)


def cleanup(video_path):

    if os.path.exists(video_path):
        os.remove(video_path)

    for f in os.listdir(FRAME_DIR):
        os.remove(os.path.join(FRAME_DIR, f))


@app.post("/upload")
async def upload_video(file: UploadFile):

    video_id = str(uuid.uuid4())

    video_path = f"{UPLOAD_DIR}/{video_id}.mp4"

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    frames = extract_frames(video_path)

    probability = analyze_frames(frames)

    cleanup(video_path)

    reasons = []

    if probability > 0.7:
        reasons.append("visual inconsistencies detected")

    if probability > 0.5:
        reasons.append("frame confidence anomaly")

    return {
        "ai_probability": round(probability,3),
        "frames_analyzed": len(frames),
        "reasons": reasons
    }