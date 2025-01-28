from QEnc_Pio_4 import QEnc_Pio_4 as QuadratureEncoder
from ST7567 import ST7567 as LcdScreen
from neopixel import NeoPixel
from machine import SPI,PWM,Pin
from time import ticks_ms



btn         = Pin(8,Pin.IN)
resetBtn    = Pin(9,Pin.IN,Pin.PULL_UP)
enA         = Pin(10,Pin.IN,Pin.PULL_UP)
enB         = Pin(11,Pin.IN,Pin.PULL_UP)

lcdBuzzer   = Pin(12,Pin.OUT)
lcdEn       = Pin(13,Pin.OUT)
lcdSck      = Pin(14,Pin.OUT)
lcdMosi     = Pin(15,Pin.OUT)

lcdD4       = Pin(20,Pin.OUT)
lcdD5       = Pin(21,Pin.OUT)
lcdRs       = Pin(22,Pin.OUT)

knob = QuadratureEncoder([enA,enB])

spi = SPI(1,baudrate=5_000_000, polarity=1, phase=1, sck=lcdSck, mosi=lcdMosi)#under 20Mhz is OK
lcd = LcdScreen(spi,a0=lcdRs,cs=lcdEn,rst=lcdD4,elecvolt=0x1F,regratio=0x03,invX=True,invY=False,invdisp=False)

neopixel = NeoPixel(lcdD5,3)
neopixel[0] = (255,255,255) # type: ignore
neopixel.write()

buzzer = PWM(lcdBuzzer,freq=4000)

defaultColor = (255,255,255)   
thresholdValue = 0
knobValueOld=0
displayValue=0
tOld=ticks_ms()

time_ms0 = ticks_ms()
while True:
    knobValue = -knob.read()
    diffKnob = knobValue-knobValueOld
    knobBtnValue = btn()
    rstBtnValue =  resetBtn()
    
    if knobBtnValue==0:
        neopixel[0] = (255,0,0) # type: ignore
        thresholdValue = thresholdValue+diffKnob
        
    else:
        neopixel[0] = defaultColor         # type: ignore
        displayValue = displayValue+diffKnob

    neopixel[1] = (255,255,255) # type: ignore
    neopixel.write()
    
    if displayValue>=thresholdValue:
        defaultColor = (255,255,255)
        buzzer.duty_u16(0)
    else:
        defaultColor = (0,255,0)
        buzzer.duty_u16(32000)
        

            
    lcd.fill(0)
    lcd.text("Encoder:",0,0,1)
    lcd.text("BTN1   :",0,10,1)
    lcd.text("BTN2   :",0,20,1)
    lcd.text("LIMIT  :",0,30,1)
    
    ticks = ticks_ms()
    frameRate = round(1000/(ticks-tOld),1)
    lcd.text(str(displayValue),100-(len(str(displayValue))-1)*8,0,1)
    lcd.text(str(knobBtnValue),100-(len(str(knobBtnValue))-1)*8,10,1)
    lcd.text(str(rstBtnValue),100-(len(str(rstBtnValue))-1)*8,20,1)
    lcd.text(str(thresholdValue),100-(len(str(thresholdValue))-1)*8,30,1)
    lcd.text(str(frameRate),100-(len(str(frameRate))-1)*8,40,1)
    lcd.show()
    knobValueOld = knobValue
    tOld = ticks

        

        


