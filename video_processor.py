import cv2

FRAME_DIR = "frames"

def extract_frames(video):

    frames = []

    cap = cv2.VideoCapture(video)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frame_interval = fps * 3

    count = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if count % frame_interval == 0:
            frames.append(frame)

        count += 1

    cap.release()

    return frames