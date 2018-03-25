import random

majorChord = [0, 4, 7]
minorChord = [0, 3, 7]
dimChord = [0, 3, 6]
augChord = [0, 4, 8]

majorChord7 = [0, 4, 7, 11]
minorChord7 = [0, 3, 7, 10]
domChord7 = [0, 4, 7, 10]
dimChord7 = [0, 3, 6, 9]
halfDimChord7 = [0, 3, 6, 10]

chordProgressions = [
    ("La Bomba",
     [
         (majorChord, 1),
         (majorChord, 4),
         (majorChord7, 5)
     ]),
    ("Rock and Roll",
     [
         (majorChord, 1),
         (majorChord, 4),
         (majorChord, 5)
     ]),
    ("You are not alone",
     [
         (majorChord, 1),
         (minorChord, 6),
         (minorChord, 2),
         (majorChord, 5)
     ]),
    ("Canon in D",
     [
         (majorChord, 1),
         (majorChord, 5),
         (minorChord, 6),
         (minorChord, 3),
         (majorChord, 4),
     ]),
    ("50's Progression",
     [
         (majorChord, 1),
         (minorChord, 6),
         (majorChord, 4),
         (majorChord, 5)
     ]),
    ("With or without you",
     [
         (majorChord, 1),
         (majorChord, 5),
         (minorChord, 6),
         (majorChord, 4)
     ])
]
dumb = [
    ("Circle Progression",
     [
         (minorChord, 6),
         (minorChord, 2),
         (majorChord, 5),
         (majorChord, 1)
     ]),
    ("Brown Eyed Girl",
     [
         (majorChord, 1),
         (majorChord, 4),
         (majorChord, 1),
         (majorChord, 5)
     ]),
    ("Standard 3",
     [
         (majorChord, 1),
         (minorChord, 6),
         (majorChord, 4),
         (majorChord, 5)
     ]),
    ("Standard 4",
     [
         (majorChord, 1),
         (minorChord, 6),
         (minorChord, 2),
         (majorChord, 5)
     ]),
    ("Shit just sounds like magic",
     [
         (majorChord, 1),
         (majorChord, 6),
         (majorChord, 3),
         (majorChord, 7)
     ]),
    ("Noise Storm - This Feeling",
     [
         (majorChord, 6),
         (majorChord, 3),
         (majorChord, 4),
         (majorChord, 1)
     ])
]

first = True
progression = 0
index = 0


def init():
    global progression, index, first

    if first:
        first = False
        random.seed()

    progression = random.randrange(len(chordProgressions))
    index = 0

    print("Selecting chord progression \"" + chordProgressions[progression][0] + "\"")


def get_next():
    global progression, index, chordProgressions

    chord = chordProgressions[progression][1][index]

    notes = []
    for i in range(len(chord[0])):
        notes.append(chord[0][i] + chord[1] - 1)

    thisIndex = index;
    index = (index + 1) % len(chordProgressions[progression][1])

    return notes, (thisIndex, len(chordProgressions[progression][1]))
