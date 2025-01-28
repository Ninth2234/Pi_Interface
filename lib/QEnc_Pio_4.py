# Quadrature encoder for RPi 2040 PIO
#
# Resolution: 4 in-/decrements per cycle.
#
# Original version (c) 2021 pmarques-dev @ github
#   (https://github.com/raspberrypi/pico-examples/blob/master/pio/quadrature_encoder/quadrature_encoder.pio).
# Adapted and modified for micropython 2022 by rkompass.
#
# Quadrature encoding uses a state table in form of a jump table
#   which is fast and has no interrupts.
# This program was reduced to take 'only' 25 of 32 available PIO instructions.
# The jump table has to reside at the beginning of PIO program memory, therefore
#   the instructions are filled up with 7 nop()'s.
# 
# The counter x is permanently pushed nonblockingly to the FIFO.
# Reading the actual value requires emptying the FIFO then waiting for and getting the next pushed value.

# The worst case sampling loop takes 14 cycles, so this program is able to read step
#   rates up to sysclk / 14  (e.g., sysclk 125MHz, max step rate = 8.9 Msteps/sec).
#
# SPDX-License-Identifier: BSD-3-Clause
#
#
# --------------------------------------------------------
#
#  Example of usage:
#  -----------------
# #
# # pinA = Pin(8, Pin.OUT)          #  Pins for generation of the quadrature signal, if you do not want to use switches.
# # pinB = Pin(9, Pin.OUT)          #  Then connect pin 6 with pin 8, and pin 7 with pin 9 on the Raspi Pico.
# # qgen = QGen_Pio((pinA, pinB), 250, freq=60_000)
# 
# pinX = Pin(6, Pin.IN, Pin.PULL_UP)
# pinY = Pin(7, Pin.IN, Pin.PULL_UP)
# qenc = QEnc_Pio_4((pinX, pinY), freq=125_000_000)
# 
# # qgen.start()
# for i in range(200):
#     print('x:', qenc.read())# , qgen.running())
#     sleep_ms(100)
# 
# --------------------------------------------------------


from rp2 import PIO, StateMachine, asm_pio

# -----  Quadrature encoder class, using RPI2040 PIO. Resolution: 4 in-/decrements per cycle  --------

class QEnc_Pio_4:
    def __init__(self, pins, sm_id=0, freq=10_000_000):
        if not isinstance(pins, (tuple, list)) or len(pins) != 2:
            raise ValueError('2 successive pins required')
        in_base = pins[0]
        self.qenc = StateMachine(sm_id, self.sm_qenc, freq=freq, in_base=in_base)
        self.qenc.exec("set(x, 0)")  # instead of sm_qenc.restart()
        self.qenc.exec("in_(pins, 2)")
        self.qenc.active(1)
    
    @asm_pio(in_shiftdir=PIO.SHIFT_LEFT, out_shiftdir=PIO.SHIFT_RIGHT)
    def sm_qenc():         #             AB    AB     !!! *** this logic is wrong, it's BA, the lower pin always is on the right side                           
        jmp("read")        # 0000 : from 00 to 00 = no change               
        jmp("decr")        # 0001 : from 00 to 01 = backward                
        jmp("incr")        # 0010 : from 00 to 10 = forward             
        jmp("read")        # 0011 : from 00 to 11 = error               
        jmp("incr")        # 0100 : from 01 to 00 = forward             
        jmp("read")        # 0101 : from 01 to 01 = no change               
        jmp("read")        # 0110 : from 01 to 10 = error               
        jmp("decr")        # 0111 : from 01 to 11 = backward                
        jmp("decr")        # 1000 : from 10 to 00 = backward                
        jmp("read")        # 1001 : from 10 to 01 = error               
        jmp("read")        # 1010 : from 10 to 10 = no change               
        jmp("incr")        # 1011 : from 10 to 11 = forward             
        jmp("read")        # 1100 : from 11 to 00 = error               
        jmp("incr")        # 1101 : from 11 to 01 = forward             
        label("decr")               
        jmp(x_dec, "read") # 1110 : from 11 to 10 = backward    !!! we cannot change all incr <-> decr because
        label("read")      # 1111 : from 11 to 11 = no change   !!! this next read has to be here after a decrement
        mov(osr, isr)      # save last pin input in OSR
        mov(isr, x)
        push(noblock)
        out(isr, 2)        # 2 right bits of OSR into ISR, all other 0
        in_(pins, 2)       # combined with current reading of input pins
        mov(pc, isr)       # jump into jump-table at addr 0
        label("incr")      # increment x by inverting, decrementing and inverting
        mov(x, invert(x))
        jmp(x_dec, "here")
        label("here")
        mov(x, invert(x))
        jmp("read")        
        nop()
        nop()
        nop()
        nop()
        nop()
        nop()
        nop()

    def read(self):
        for _ in range(self.qenc.rx_fifo()):
            self.qenc.get()
        n = self.qenc.get()
        return -n if n < (1<<31) else (1<<32)-n  #  !!! *** therefore we change the polarity of counting here
if __name__ == "__main__":
    from machine import Pin
    from time import sleep
    pinA = Pin(8, Pin.IN)
    pinB = Pin(9, Pin.IN)
    encoder = QEnc_Pio_4((pinA, pinB), sm_id = 7, freq = machine.freq())
    while True:
        print(encoder.read())
        sleep(0.1)