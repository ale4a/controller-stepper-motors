import os
import time

os.system("pip3 install keyboard")
import keyboard
while True:
    if keyboard.is_pressed('space'): 
        print('Keyboard library works... Awesome!')
        break

os.system("pip install pyfirmata")
import pyfirmata
board = pyfirmata.Arduino('COM4')
while True:
    if keyboard.is_pressed('space'):
        board.digital[13].write(1)
        time.sleep(0.1)
    else:
        board.digital[13].write(0)
        time.sleep(0.1)