import signal
import sys
import time
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
UDP_PORT = 5005

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
    melody_off_msg = None
    bass_off_msg = None
    start_time = time.perf_counter()
    to_time = start_time + s_per_sixteenth

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        chord, chord_progress = ChordGen.get_next()
        for msg in make_chord_msgs(chord, key, 100, transposition, chan_harmony):
            out_port.send(msg)

        chord_net_msg = {'instrument': 'harmony',
            'chord': (chord, chord_progress)}
        sock.sendto(pickle.dumps(chord_net_msg), (UDP_IP, UDP_PORT))

        melody_notes, melody_rhythms = melody_gen.get_next(chord)
        bass_notes, bass_rhythms = Bassline.get_next(chord)
        drum_notes, drum_rhythms = DrumMachine.get_next()

        drum_idx = 0
        melody_idx = 0
        melody_dur_remaining = 0
        bass_idx = 0
        bass_dur_remaining = 0
        for sixteenth in range(16):
            # Percussion
            if drum_idx < len(drum_rhythms) and drum_rhythms[drum_idx] == sixteenth:
                for msg in make_chord_msgs(drum_notes[drum_idx], 0, 0, transposition, chan_percussion):
                    out_port.send(msg)
                for msg in make_chord_msgs(drum_notes[drum_idx], 0, 100, transposition, chan_percussion):
                    out_port.send(msg)

                percussion_net_msg = {perc_inst_mapping[note]: True for note in drum_notes[drum_idx]}
                percussion_net_msg['instrument'] = 'percussion'
                sock.sendto(pickle.dumps(percussion_net_msg), (UDP_IP, UDP_PORT))

                drum_idx += 1

            # Melody
            if melody_dur_remaining == 0:
                if melody_off_msg is not None:
                    out_port.send(melody_off_msg)
                    melody_off_msg = None
                note_pair = melody_notes[melody_idx]
                midi_note = octave_to_note(note_pair[1], note_pair[0])
                start_msg = make_chord_msgs([midi_note], key, 100, transposition, chan_melody)[0]
                out_port.send(start_msg)
                melody_net_msg = {'instrument': 'melody',
                              'note': note_pair[0]}
                sock.sendto(pickle.dumps(melody_net_msg), (UDP_IP, UDP_PORT))

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
                    sock.sendto(pickle.dumps(bass_net_msg), (UDP_IP, UDP_PORT))

            sleep_for = max(0, to_time - time.perf_counter())
            print(sleep_for)
            time.sleep(sleep_for)
            to_time += s_per_sixteenth
            melody_dur_remaining -= 1
            bass_dur_remaining -= 1
            # note_status['melody']['time'] += s_per_sixteenth


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

# process = None
# process_running = Value('i', 0)
# def start_async():
#     global process
#     process_running.value = 1
#     process = Process(target = start, args=(process_running,False))
#     process.start()
#
# def stop_async():
#     global process_running
#     process_running.value = 0
#     process.join()

def no_cb(*args, **kwargs):
    pass
callbacks = defaultdict(lambda: no_cb)
def set_melody_callback(cb):
    callbacks['melody'] = cb

if __name__ == '__main__':
    thread_running = True
    start(True)
    # start_async()
    # time.sleep(10)
    # stop_async()