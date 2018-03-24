import ChordGen
import time

ChordGen.init()

while True:
    print(ChordGen.get_next())
    time.sleep(1)
