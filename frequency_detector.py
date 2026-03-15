import cv2
import numpy as np

def frequency_score(frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    fft = np.fft.fft2(gray)

    magnitude = np.log(np.abs(fft)+1)

    score = magnitude.mean()

    # normalize to 0–1 range
    normalized = score / 50

    return min(normalized, 1.0)