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
    ("50's Progression",
     [
         (majorChord, 1),
         (minorChord, 6),
         (majorChord, 4),
         (majorChord, 5)
     ]),
    ("Circle Progression",
     [
         (minorChord, 6),
         (minorChord, 2),
         (majorChord, 5),
         (majorChord, 1)
     ])
]

progression = 0
index = 0


def init():
    global progression, index

    progression = (progression + 1) % len(chordProgressions)
    index = 0

    print("Selecting chord progression \"" + chordProgressions[progression][0] + "\"")


def get_next():
    global progression, index, chordProgressions

    chord = chordProgressions[progression][1][index]

    notes = []
    for i in range(len(chord[0])):
        notes.append(chord[0][i] + chord[1])

    print(index)
    index = (index + 1) % len(chordProgressions[progression][1])

    return notes
