import subprocess
import os

FRAME_DIR = "frames"

def extract_frames(video_path):

    os.makedirs(FRAME_DIR, exist_ok=True)

    subprocess.run([
        "ffmpeg",
        "-i", video_path,
        "-vf", "fps=1",
        f"{FRAME_DIR}/frame_%04d.jpg"
    ])

    frames = [f for f in os.listdir(FRAME_DIR) if f.endswith(".jpg")]

    return frames