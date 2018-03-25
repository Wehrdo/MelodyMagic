import pickle
import socket
import random
import bge

cont = bge.logic.getCurrentController()
obj = cont.owner
scene = bge.logic.getCurrentScene()
# if not 'initialized' in obj:
#     sys.path.append('../source')
# import core

if not 'initialized' in obj:
    obj['sock'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obj['sock'].bind(('127.0.0.1', 5005))
    obj['sock'].setblocking(False)

    obj['circles'] = [scene.objects['note' + str(i+1)] for i in range(12)]
    for circle in obj['circles']:
        circle.setVisible(False)

    obj['kick'] = scene.objects['kick']
    obj['initialized'] = True



received = bytes()
try:
    received = obj['sock'].recv(1024)
except:
    pass
if len(received):
    data = pickle.loads(received)
    if data['instrument'] == 'melody':
        note = data['note']
        print("adding", note)
        circle = obj['circles'][note % len(obj['circles'])]
        new_obj = scene.addObject('note_halo', circle, 50)
        circle_color = circle.meshes[0].materials[0].diffuseColor
        new_obj.color = [circle_color.r, circle_color.g, circle_color.b, 1]
        variance = 0.0
        new_obj.worldPosition.x += variance * random.random()
        new_obj.worldPosition.y += variance * random.random()
        new_obj.worldPosition.z += 0.1

    if 'kick' in data:
        pass

