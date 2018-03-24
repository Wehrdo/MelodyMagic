import DrumMachine
import time

DrumMachine.init()

while True:
    notes, rhythym = DrumMachine.get_next()

    print(notes)
    print(rhythym)
    print()

    time.sleep(2)