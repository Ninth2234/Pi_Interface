from machine import Pin
from time import sleep


pin26 = Pin(26,Pin.IN,Pin.PULL_UP)


while True:

    print(pin26())
    sleep(0.1)