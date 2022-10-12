# arduino_LED_user.py

import serial
import time

# Define the serial port and baud rate.
# Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
ser = serial.Serial('COM7', 9600)

def led_on_off():
    print("R: Right - clockwise")
    print("L: Left  - counterclockwise")
    
    user_input = input("\n Type R / L / quit : ")
    if user_input =="R":
        print("clockwise...")
        time.sleep(0.1) 
        ser.write(b'R') 
        led_on_off()
    elif user_input =="L":
        print("counterclockwise...")
        time.sleep(0.1)
        ser.write(b'L')
        led_on_off()
    elif user_input =="quit" or user_input == "q":
        print("Program Exiting")
        time.sleep(0.1)
        ser.close()
    else:
        print("Invalid input. Type on / off / quit.")
        led_on_off()

time.sleep(2) # wait for the serial connection to initialize

led_on_off()
