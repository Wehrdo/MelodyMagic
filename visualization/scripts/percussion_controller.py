import pickle
import socket
import random
import bge

cont = bge.logic.getCurrentController()
obj = cont.owner
scene = bge.logic.getCurrentScene()

if not 'initialized' in obj:
    obj['sock'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obj['sock'].bind(('127.0.0.1', 5005))
    obj['sock'].setblocking(False)

    obj['kick'] = scene.objects['kick']
    obj['initialized'] = True


received = bytes()
try:
    received = obj['sock'].recv(1024)
except:
    pass
if len(received):
    data = pickle.loads(received)
    if 'kick' in data:
        print("bass")
