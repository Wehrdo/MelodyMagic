import signal
import sys
import time
import mido
import ChordGen
from melody import MelodyGen
import DrumMachine

chan_melody = 0
chan_harmony = 1
chan_percussion = 3

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
    while True:
        chord = ChordGen.get_next()
        for msg in make_chord_msgs(chord, key, 100, transposition, chan_harmony):
            out_port.send(msg)

        melody_notes, melody_rhythms = melody_gen.get_next(chord)

        drum_notes, drum_rhythms = DrumMachine.get_next()
        drum_idx = 0
        melody_idx = 0
        melody_dur_remaining = 0
        melody_off_msg = None
        for sixteenth in range(16):
            # Percussion
            if drum_idx < len(drum_rhythms) and drum_rhythms[drum_idx] == sixteenth:
                for msg in make_chord_msgs(drum_notes[drum_idx], 0, 100, transposition, chan_percussion):
                    out_port.send(msg)
                drum_idx += 1

            # Melody
            if melody_dur_remaining == 0:
                if melody_off_msg is not None:
                    out_port.send(melody_off_msg)
                note_pair = melody_notes[melody_idx]
                midi_note = octave_to_note(note_pair[1], note_pair[0])
                start_msg = make_chord_msgs([midi_note], key, 100, transposition, chan_melody)[0]
                out_port.send(start_msg)

                melody_off_msg = make_chord_msgs([midi_note], key, 0, transposition, chan_melody)[0]

                melody_dur_remaining = melody_rhythms[melody_idx]
                melody_idx += 1



            time.sleep(s_per_sixteenth)
            melody_dur_remaining -= 1


        for msg in make_chord_msgs(chord, key, 0, transposition):
            out_port.send(msg)


if __name__ == '__main__':
    with mido.open_output('loopMIDI Port 1') as port:
        def signal_handler(signal, frame):
            print("sending")
            for chan in [chan_percussion, chan_harmony, chan_melody]:
                for note in range(0, 128):
                    port.send(mido.Message('note_off', note=note, channel=chan, velocity=0))
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

        run(port)
