import cv2
import numpy as np

cap = None
prevFrame = None
threshold = 5

def init():
    global cap, prevFrame

    cap = cv2.VideoCapture(0)
    prevFrame = get_frame()


def get_next():
    xFlow = get_flow()[..., 0]

    dir = 0
    intensity = 0
    mask = np.where(abs(xFlow) > threshold)

    if len(mask[0]) > 0:
        dir = -np.mean(xFlow[mask])
        intensity = np.sqrt(np.mean(np.square(xFlow[mask])))
    else:
        print("No values")

    #map = ((abs(xFlow) > threshold) * 255).astype(np.float32)
    #cv2.imshow("thresholded", cv2.cvtColor(map, cv2.COLOR_GRAY2BGR))

    return dir, intensity


def get_frame():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (320, 240))
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def get_flow():
    global prevFrame
    curFrame = get_frame()
    # 3
    flow = cv2.calcOpticalFlowFarneback(prevFrame, curFrame, None, 0.5, 1, 15, 3, 5, 1.2, 0)

    prevFrame = curFrame
    return flow


