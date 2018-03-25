import serial

device = None

def init(port):
    global device

    device = serial.Serial(port, 115200, timeout=0)


def send_update(updateType, chord_progress, chord):
    chord = chord[:]
    if len(chord) < 4:
        chord.append(*([255] * (4-len(chord))))
    elif len(chord) > 4:
        chord = chord[range(4)]

    msg = bytes([updateType, *chord_progress, *chord, 0])
    device.write(msg)


def read_device():
    return device.read(1024)
