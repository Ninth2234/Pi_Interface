from machine import SPI, Pin
from neopixel import NeoPixel
from ST7567 import ST7567

lcdEn     = Pin(13, Pin.OUT)  
lcdSck    = Pin(14, Pin.OUT)  
lcdMosi   = Pin(15, Pin.OUT)  

lcdD4       = Pin(20,Pin.OUT)
lcdD5       = Pin(21,Pin.OUT)
lcdRs       = Pin(22,Pin.OUT)

spi = SPI(1,baudrate=5_000_000, polarity=1, phase=1, sck=lcdSck, mosi=lcdMosi)
lcd = ST7567(spi,a0=lcdRs,cs=lcdEn,rst=lcdD4,elecvolt=0x2F,regratio=0x03,invX=False,invY=True,invdisp=False)


neopixel = NeoPixel(lcdD5,3)
neopixel[0] = (255,255,255) 
neopixel[1] = (0,20,0) 
neopixel[2] = (20,0,0) 
neopixel.write()

lcd.fill(0)  
lcd.text("Hello World!", 10, 10, 1)  
lcd.show()

