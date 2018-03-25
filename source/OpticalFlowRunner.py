import OpticalFlow
import pickle
import socket
import time

UDP_IP = '127.0.0.1'
UDP_PORT = 5005

OpticalFlow.init()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    dir, intensity = OpticalFlow.get_next()

    msg = {"instrument":"camera",
                "motion":(dir, intensity)
    }
    sock.sendto(pickle.dumps(msg), (UDP_IP, UDP_PORT))

    print("Direction: {}, Intensity: {}".format(dir, intensity))

    time.sleep(0.03)
