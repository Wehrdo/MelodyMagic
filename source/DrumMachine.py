####Instruments###
#Kick drum: C-1         0
#Cowbell F-1            5
#Snare C#-1             1
#Clap D-1               2
#Scrape'n'slide B-1     11
#Open Hat E-1           4
#Closed Hat D#-1        3
#Tom G-1                7

import random

instruments = (
    (
        "kick", #Name
        0,  # MIDI note
        (0.8, 0.1, 0.4, 0.1, 0.8, 0.1, 0.4, 0.1, 0.8, 0.1, 0.4, 0.1, 0.8, 0.1, 0.4, 0.1),   #Hit probability for each 16th note in measure
        (1, 0)  #Relative probability for hit if not previously hit, previously hit
    ),
    (
        "snare",
        1,
        (0.5, 0.2, 0.75, 0.2, 0.5, 0.2, 0.75, 0.2, 0.5, 0.2, 0.75, 0.2, 0.5, 0.2, 0.75, 0.2),
        (1, 0.5)
    ),
    (
        "closed hat",
        3,
        (0.2, 0.75, 0.2, 0.75, 0.2, 0.75, 0.2, 0.75, 0.2, 0.75, 0.2, 0.75, 0.2, 0.75, 0.2, 0.75),
        (1, 3)
    ),
    (
        "open hat",
        4,
        (0.5, 0.1, 0.2, 0.1, 0.5, 0.1, 0.2, 0.1, 0.5, 0.1, 0.2, 0.1, 0.5, 0.1, 0.2, 0.1),
        (1, 0)
    ),
    (
        "tom",
        7,
        (0.75, 0.2, 0.5, 0.2, 0.75, 0.2, 0.5, 0.2, 0.75, 0.2, 0.5, 0.2, 0.75, 0.2, 0.5, 0.2),
        (1, 0.5)
    ),
    (
        "clap",
        2,
        (0.2, 0.3, 0.5, 0.3, 0.2, 0.3, 0.5, 0.3, 0.2, 0.3, 0.5, 0.3, 0.2, 0.3, 0.5, 0.2),
        (1, 1.5)
    )
)

notes = []
rhythym = []


def init():
    global rhythym, notes

    notes = []
    rhythym = []

    prevHits = [0] * len(instruments)
    for i in range(16):
        attacks = []
        for instrument in range(len(instruments)):
            prob = instruments[instrument][2][i] * instruments[instrument][3][prevHits[instrument]]
            if (random.random() + prob) > 1.0:
                attacks.append(instruments[instrument][1])
                prevHits[instrument] = 1
            else:
                prevHits[instrument] = 0

        if len(attacks) > 0:
            notes.append(attacks)
            rhythym.append(i)


def get_next():
    return notes, rhythym
