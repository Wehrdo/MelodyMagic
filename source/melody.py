import random
import math
import numpy as np
import scipy.stats

class MelodyGen:
    def __init__(self):
        # self.octave = 0
        # self.chord_idx = 0
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
                sep = 2.0
                scale = dim/4
                mm[i,j] += dist.cdf(j+0.5, loc=i-sep, scale=scale) - \
                          dist.cdf(j-0.5, loc=i-sep, scale=scale)

                mm[i,j] += dist.cdf(j+0.5, loc=i+sep, scale=scale) - \
                           dist.cdf(j-0.5, loc=i+sep, scale=scale)
            # normalize
            mm[i] /= np.sum(mm[i])

        # print(mm)
        rhythm_mm = np.array([[0.4, 0.25, 0.25, 0.1],
                              [0.2, 0.3, 0.4, 0.1],
                              [0.1, 0.3, 0.5, 0.1],
                              [0.05, 0.25, 0.6, 0.1]])
        rhythm_mm_durations = [1, 2, 4, 8]

        notes = []
        rhythms = []

        pos = int(dim / 2)
        rhythm_pos = int(rhythm_mm.shape[0] / 2)
        duration = 0
        measure_duration = 16
        while duration < measure_duration:
            # Choose note duration
            # note_length = random.randint(0, min(measure_duration - duration, 16))
            rhythm_pos = np.random.choice(np.arange(0, rhythm_mm.shape[1]), p=rhythm_mm[rhythm_pos])
            note_length = rhythm_mm_durations[rhythm_pos]

            rhythms.append(note_length)
            duration += note_length

            pos = np.random.choice(np.arange(0, mm.shape[1]), p=mm[pos])
            octave = int(pos / (n_octaves * len(chord)))
            note = chord[pos % len(chord)]
            notes.append((note, octave))

            # # Step random direction
            # idx_step = random.randint(-1, 1)
            # self.chord_idx += idx_step
            # # Move octave if necessary
            # self.octave += math.floor(self.chord_idx / len(chord))
            # # Wrap chord idx
            # self.chord_idx = self.chord_idx % len(chord)
            #
            # notes.append((chord[self.chord_idx], self.octave))

        return notes, rhythms
