####Instruments###
#Kick drum: F2          41
#Cowbell C#3            49
#Snare D#4              63
#Clap C#-1              1
#Scrape'n'slide A#0     22

import random

instruments = (
    41, 49, 63, 1, 22
)

probabilities = (
    0.75, 0.2, 0.5, 0.2, 0.75, 0.2, 0.5, 0.2, 0.75, 0.2, 0.5, 0.2, 0.75, 0.2, 0.5, 0
)

notes = []
rhythym = []


def init():
    global rhythym, notes

    notes = []
    rhythym = []
    for i in range(16):
        attacks = []
        for instrument in range(len(instruments)):
            if (random.random() + probabilities[i]) > 1.0:
                attacks.append(instruments[instrument])

        if len(attacks) > 0:
            notes.append(attacks)
            rhythym.append(i)


def get_next():
    return notes, rhythym
