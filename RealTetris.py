from pyboy import PyBoy, WindowEvent

import os
import sys
pyboy = PyBoy('Tetris/tetris.gb')
print("hello")
while not pyboy.tick():
    pass
pyboy.stop()