import random
import math
import numpy as np
import scipy.stats

class MelodyGen:
    def __init__(self):
        self.octave = 0
        self.chord_idx = 0
        pass

    def get_next(self, chord):
        # Generate Markov model
        n_octaves = 2
        dist = scipy.stats.norm
        dim = n_octaves * len(chord)
        mm = np.zeros((dim, dim))
        # center = int(dim/2)
        for i in range(dim):
            for j in range(dim):
                mm[i,j] = dist.cdf(j, loc=i, scale=dim/2) - \
                          dist.cdf(j-1, loc=i, scale=dim/2)
        print(mm)

        notes = []
        rhythms = []

        duration = 0
        measure_duration = 16*4
        while duration < measure_duration:
            # Choose note duration
            note_length = random.randint(0, min(measure_duration - duration, 16))
            duration += note_length
            rhythms.append(note_length)

            # Step random direction
            idx_step = random.randint(-1, 1)
            self.chord_idx += idx_step
            # Move octave if necessary
            self.octave += math.floor(self.chord_idx / len(chord))
            # Wrap chord idx
            self.chord_idx = self.chord_idx % len(chord)

            notes.append((chord[self.chord_idx], self.octave))

        return notes, rhythms
