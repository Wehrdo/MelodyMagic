import LEDMatrix
import time
import pickle
import socket

LEDMatrix.init("COM4")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5005))
sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

chord = [1, 6, 2, 5]
chord_idx = 0
while True:
    received = sock.recv(1024)

    if len(received) > 0:
        data = pickle.loads(received)

        if data['instrument'] == 'harmony':
            LEDMatrix.send_update(0, data['chord'][1], data['chord'][0])
            #print("Harmony data: {}".format(data['chord']))
        elif data['instrument'] == 'bass':
            LEDMatrix.send_update(1, data['chord'][1], data['chord'][0])
            #print("Bassline data: {}".format(data['chord']))
        else:
            sock2.sendto(pickle.dumps(data), ('127.0.0.1', 5007))
        #elif data['instrument'] == 'melody':
        #    LEDMatrix.send_update(2, (255, 255), [data['note'], 255, 255])
        #    print("Melody data: {}".format(data['note']))
