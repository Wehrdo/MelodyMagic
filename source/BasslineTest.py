import Bassline
import time

Bassline.init()
while True:
    notes, durs = Bassline.get_next([0, 4, 7])

    print(notes)
    print(durs)
    print()

    time.sleep(1)