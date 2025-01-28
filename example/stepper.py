from machine import Pin
from time import sleep



pin0 = Pin(0,Pin.OUT)
pin1 = Pin(1,Pin.OUT)
pin2 = Pin(2,Pin.OUT)
pin3 = Pin(3,Pin.OUT)

pause_time = 0.002
while True:
    for i in range(500):
        pin0.high()
        pin2.high()
        sleep(pause_time)

        pin0.low()
        pin2.low()
        sleep(pause_time)

    pin1.high()
    pin3.high()

    for i in range(500):
        pin0.high()
        pin2.high()
        sleep(pause_time)

        pin0.low()
        pin2.low()
        sleep(pause_time)