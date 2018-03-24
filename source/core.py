import time
import mido
import ChordGen
from melody import MelodyGen

def make_chord_msgs(chord, key, vel=100, transposition=0):
    messages = []
    for note in chord:
        messages.append(mido.Message('note_on', note=key+note, velocity=vel))
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
    while True:
        chord = ChordGen.get_next()
        for msg in make_chord_msgs(chord, key, 100, transposition):
            out_port.send(msg)

        melody_notes, melody_rhythms = melody_gen.get_next(chord)
        for note_pair, duration in zip(melody_notes, melody_rhythms):
            midi_note = octave_to_note(note_pair[1], note_pair[0])
            start_msg = make_chord_msgs([midi_note], key, 100, transposition)[0]
            out_port.send(start_msg)
            time.sleep(s_per_sixteenth * duration)
            end_msg = make_chord_msgs([midi_note], key, 0, transposition)[0]
            out_port.send(end_msg)

        for msg in make_chord_msgs(chord, key, 0, transposition):
            out_port.send(msg)


if __name__ == '__main__':
    with mido.open_output('loopMIDI Port 1') as port:
        run(port)