import cv2
import os

FRAME_DIR = "frames"

def extract_frames(video):

    os.makedirs(FRAME_DIR, exist_ok=True)

    frames = []

    cap = cv2.VideoCapture(video)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    interval = fps * 3

    count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        if count % interval == 0:

            path = f"{FRAME_DIR}/frame_{count}.jpg"

            cv2.imwrite(path, frame)

            frames.append(path)

        count += 1

    cap.release()

    return frames