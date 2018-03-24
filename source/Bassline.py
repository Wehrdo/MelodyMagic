import random

rhythym = []

def init():
    global rhythym

    dur = 2 ** random.randrange(1, 5)

    total = 0
    while total < 16:
        rhythym.append(dur)
        total = total + dur


def get_next(chord):
    # Single whole note
    notes = [chord[0]] * len(rhythym)

    return notes, rhythym