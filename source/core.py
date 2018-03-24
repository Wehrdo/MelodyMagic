import time
import mido
import ChordGen
from melody import MelodyGen

def make_chord_msgs(chord, key, vel=100, transposition=0):
    messages = []
    for note in chord:
        messages.append(mido.Message('note_on', note=key+note, velocity=vel))
    return messages

def run(out_port):
    melody_gen = MelodyGen()
    transposition = 0
    key = 60 # middle C = 60
    tempo = 100
    s_per_sixteenth = 1 / (16 * tempo / 60)
    ChordGen.init()
    while True:
        chord = ChordGen.get_next()
        for msg in make_chord_msgs(chord, key, 100, transposition):
            out_port.send(msg)

        # melody_notes, melody_rhythms = melody_gen.get_next()

        for beat in range(1, 4):
            for sixteenth in range(16):
                # TODO: Run a global timer instead of sleep
                time.sleep(s_per_sixteenth)

        for msg in make_chord_msgs(chord, key, 0, transposition):
            out_port.send(msg)
        chord = [note+1 for note in chord]


if __name__ == '__main__':
    with mido.open_output('loopMIDI Port 1') as port:
        run(port)