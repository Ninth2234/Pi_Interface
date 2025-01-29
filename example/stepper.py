from machine import Pin
from time import sleep

stp = Pin(0,Pin.OUT)
dir = Pin(1,Pin.OUT)

delay_time = 0.02
step = 100
while True:
    dir.on()
    for i in range(step):
        stp.on()
        sleep(delay_time/2)
        stp.off()
        sleep(delay_time/2)
    dir.off()
    for i in range(step):
        stp.on()
        sleep(delay_time/2)
        stp.off()
        sleep(delay_time/2)        