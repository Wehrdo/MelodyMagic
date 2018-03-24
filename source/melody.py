import random

class MelodyGen:
    def __init__(self):
        self.octave = 4
        self.chord_idx = 0
        pass

    def get_next(self, chord):
        notes = []
        rhythms = []

        duration = 0
        measure_duration = 16*4
        while duration < measure_duration:
            note_length = random.randint(0, min(measure_duration - duration, 16))

        return notes, rhythms
