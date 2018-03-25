import OpticalFlow
import cv2

OpticalFlow.init()

while True:
    dir, intensity = OpticalFlow.get_next()

    print("Direction: {}, Intensity: {}".format(dir, intensity))

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
