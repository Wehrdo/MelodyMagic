import pickle
import socket
import random
import math
import bge
import scipy.stats

cont = bge.logic.getCurrentController()
obj = cont.owner
scene = bge.logic.getCurrentScene()
# if not 'initialized' in obj:
#     sys.path.append('../source')
# import core

if not 'initialized' in obj:
    obj['sock'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    obj['sock'].bind(('127.0.0.1', 5007))
    obj['sock'].setblocking(False)

    obj['circles'] = [scene.objects['note' + str(i+1)] for i in range(12)]
    for circle in obj['circles']:
        circle.setVisible(False)

    obj['boop'] = scene.objects['boop']
    instruments =        ['kick', 'tom', 'snare', 'open hat']
    obj['perc_decays'] = [0.875,     0.9,    0.85,    0.95]
    obj['inst_map'] = {inst_name: i for i, inst_name in enumerate(instruments)}
    # position 0 is bottom of circle, 1 is top
    offsets = [0, 0.33, 0.66, 1.0]
    # x-scale of standard normal distribution
    widths = [0.1, 0.07, 0.07, 0.1]
    res = 128
    scale = 3.5
    obj['perc_peaks'] = []
    obj['perc_vals'] = []
    for i in range(len(instruments)):
        max_vals = [1.0] * res
        obj['perc_peaks'].append(max_vals)
        perc_val = [1.0] * res
        obj['perc_vals'].append(perc_val)
        width = widths[i]
        offset = offsets[i]
        for j in range(res):
            norm_j = j / res
            pdf_val = scipy.stats.norm.pdf((norm_j - offset) / width)
            max_vals[j] += scale * pdf_val
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

    if data['instrument'] == 'percussion':
        for inst_name in data['hits']:
            inst_id = obj['inst_map'][inst_name]
            peaks = obj['perc_peaks'][inst_id]
            perc_val = obj['perc_vals'][inst_id]
            for i in range(len(perc_val)):
                perc_val[i] = peaks[i]

# Shape the boop
boop_mesh = obj['boop'].meshes[0]
for v_index in range(boop_mesh.getVertexArrayLength(0)):
    res = len(obj['perc_vals'][0])
    vert = boop_mesh.getVertex(0, v_index)
    angle = math.atan2(abs(vert.x), -vert.y)
    # angle = math.atan2(vert.y, vert.x)
    # betweeen 0 and 1
    # norm_angle = (angle + math.pi/2) / math.pi
    norm_angle = angle / math.pi
    idx = int(norm_angle * (res-1))
    scale_sum = 0
    for perc_val in obj['perc_vals']:
        scale_sum += perc_val[idx]
    scale = scale_sum / len(obj['perc_vals'])
    true_angle = math.atan2(vert.y, vert.x)
    new_pos = [scale * math.cos(true_angle), scale * math.sin(true_angle), 0]
    vert.setXYZ(new_pos)


# Decay percussion
for inst_id in range(len(obj['perc_decays'])):
    decay_rate = obj['perc_decays'][inst_id]
    perc_val = obj['perc_vals'][inst_id]
    for i in range(len(perc_val)):
        perc_val[i] = (decay_rate * (perc_val[i] - 1)) + 1
