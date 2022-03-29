from machine import Pin, ADC, unique_id
from time import sleep
import random
red_left = Pin(32, Pin.OUT)

yellow_left = Pin(33, Pin.OUT)
red_right = Pin(25, Pin.OUT)
yellow_right = Pin(26, Pin.OUT)
blue = Pin(27, Pin.OUT)

    

def led_tester(amount=1):
    global red_left, yellow_left, red_right, yellow_right, blue
    for x in range(amount):
        for led in [red_left, yellow_left, red_right, yellow_right, blue]:
            led.value(1)
            sleep(0.5)
            led.value(0)
            
try: 
    led_tester()
    

except KeyboardInterrupt: 
    print("Stopping program")
    exit()