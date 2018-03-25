import signal
import sys
import time
import math
import socket
from collections import defaultdict
import pickle
import mido
import ChordGen
from melody import MelodyGen
import DrumMachine
import Bassline

chan_melody = 0
chan_harmony = 1
chan_percussion = 9
chan_bass = 3

perc_inst_mapping = {inst[1]: inst[0] for inst in DrumMachine.instruments}

UDP_IP = '127.0.0.1'
UDP_PORT_SENDS = [5005, 5009]
UDP_PORT_RECV = 5007

thread_running = False
# note_status = {'melody': {'time': 0},
#                'percussion': {},
#                'bass': {},
#                'harmony': {}}

def make_chord_msgs(chord, key, vel=100, transposition=0, channel=1):
    messages = []
    for note in chord:
        messages.append(mido.Message('note_on', note=key+note, velocity=vel, channel=channel))
    return messages

def octave_to_note(octave, note_offset):
    octave_root = 12 * octave
    return octave_root + note_offset

def run(out_port):
    melody_gen = MelodyGen()
    transposition = 0
    key = 60 # middle C = 60
    tempo = 100
    s_per_sixteenth = 60 / (4 * tempo)
    ChordGen.init()
    DrumMachine.init()
    Bassline.init()
    n_octaves = 4
    dir_decay = 0.9
    dir_scale = 0.4
    melody_dir = 0
    melody_intensity = 0
    melody_off_msg = None
    bass_off_msg = None
    start_time = time.perf_counter()
    to_time = start_time + s_per_sixteenth

    sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_recv.bind((UDP_IP, UDP_PORT_RECV))
    sock_recv.setblocking(False)
    sock_sends = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for r in UDP_PORT_SENDS]

    def recv_of():
        received = bytes()
        try:
            while True:
                new_recv = sock_recv.recv(1024)
                if len(new_recv):
                    received = new_recv
                else:
                    break
        except socket.error:
            pass

        flow = (0, 0)
        if len(received):
            data = pickle.loads(received)
            if data['instrument'] == 'camera':
                flow = data['motion']
        return flow


    while True:
        chord, chord_progress = ChordGen.get_next()
        for msg in make_chord_msgs(chord, key, 100, transposition, chan_harmony):
            out_port.send(msg)

        chord_net_msg = {'instrument': 'harmony',
            'chord': (chord, chord_progress)}
        for i, sock_send in enumerate(sock_sends):
            sock_send.sendto(pickle.dumps(chord_net_msg), (UDP_IP, UDP_PORT_SENDS[i]))

        melody_notes, melody_rhythms = melody_gen.get_next(chord)
        bass_notes, bass_rhythms = Bassline.get_next(chord)
        drum_notes, drum_rhythms = DrumMachine.get_next()

        drum_idx = 0
        melody_idx = 0
        melody_dur_remaining = 0
        bass_idx = 0
        bass_dur_remaining = 0
        for sixteenth in range(16):
            # Optical flow
            new_dir, new_intensity = recv_of()
            melody_dir += dir_scale * new_dir
            print(melody_dir)

            # Percussion
            if drum_idx < len(drum_rhythms) and drum_rhythms[drum_idx] == sixteenth:
                for msg in make_chord_msgs(drum_notes[drum_idx], 0, 0, transposition, chan_percussion):
                    out_port.send(msg)
                for msg in make_chord_msgs(drum_notes[drum_idx], 0, 100, transposition, chan_percussion):
                    out_port.send(msg)

                percussion_net_msg = {'instrument': 'percussion'}
                percussion_net_msg['hits'] = {perc_inst_mapping[note]: True for note in drum_notes[drum_idx]}
                for i, sock_send in enumerate(sock_sends):
                    sock_send.sendto(pickle.dumps(percussion_net_msg), (UDP_IP, UDP_PORT_SENDS[i]))

                drum_idx += 1

            # Melody
            if melody_dur_remaining == 0:
                if melody_off_msg is not None:
                    out_port.send(melody_off_msg)
                    melody_off_msg = None
                chord_pos = melody_notes[melody_idx]
                chord_pos += round(float(melody_dir))
                octave = math.floor(chord_pos / (n_octaves * len(chord)))
                note = chord[chord_pos % len(chord)]
                print(note, octave)
                midi_note = octave_to_note(octave, note)
                start_msg = make_chord_msgs([midi_note], key, 100, transposition, chan_melody)[0]
                out_port.send(start_msg)
                melody_net_msg = {'instrument': 'melody',
                              'note': note}
                for i, sock_send in enumerate(sock_sends):
                    sock_send.sendto(pickle.dumps(melody_net_msg), (UDP_IP, UDP_PORT_SENDS[i]))

                melody_off_msg = make_chord_msgs([midi_note], key, 0, transposition, chan_melody)[0]

                melody_dur_remaining = melody_rhythms[melody_idx]
                melody_idx += 1


            # Bass
            if bass_dur_remaining == 0:
                if bass_off_msg is not None:
                    out_port.send(bass_off_msg)
                    bass_off_msg = None
                note = bass_notes[bass_idx]
                midi_note = octave_to_note(0, note)
                start_msg = make_chord_msgs([midi_note], key, 100, transposition, chan_bass)[0]
                out_port.send(start_msg)

                bass_off_msg = make_chord_msgs([midi_note], key, 0, transposition, chan_bass)[0]

                bass_dur_remaining = bass_rhythms[bass_idx]
                bass_idx += 1

                if sixteenth > 0:
                    bass_net_msg = {'instrument': 'bass',
                        'chord': (chord, chord_progress)}
                    for i, sock_send in enumerate(sock_sends):
                        sock_send.sendto(pickle.dumps(bass_net_msg), (UDP_IP, UDP_PORT_SENDS[i]))

            melody_dur_remaining -= 1
            bass_dur_remaining -= 1
            melody_dir *= dir_decay

            sleep_for = max(0, to_time - time.perf_counter())
            time.sleep(sleep_for)
            to_time += s_per_sixteenth


        for msg in make_chord_msgs(chord, key, 0, transposition):
            out_port.send(msg)
    stop_all(out_port)

def stop_all(port):
    for chan in [chan_percussion, chan_harmony, chan_melody, chan_bass]:
        for note in range(0, 128):
            port.send(mido.Message('note_off', note=note, channel=chan, velocity=0))


def start(register_sigint):
    with mido.open_output('loopMIDI Port 1') as port:
        if register_sigint:
            def signal_handler(signal, frame):
                stop_all(port)
                sys.exit(0)
            signal.signal(signal.SIGINT, signal_handler)
        run(port)


def no_cb(*args, **kwargs):
    pass
callbacks = defaultdict(lambda: no_cb)
def set_melody_callback(cb):
    callbacks['melody'] = cb

if __name__ == '__main__':
    thread_running = True
    start(True)
