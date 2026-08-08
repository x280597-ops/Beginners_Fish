from machine import Pin, SPI
import time
import st7789
def color565(r, g, b):
    return (
        ((r & 0xf8) << 8) |
        ((g & 0xfc) << 3) |
        (b >> 3)
    )
BLACK = color565(0,0,0)
WHITE = color565(255,255,255)
RED   = color565(255,0,0)
GREEN = color565(0,255,0)
BLUE  = color565(0,0,255)
class Display():
    def __init__(self):
        self.spi = SPI( 0,baudrate=40000000,polarity=1,phase=1,sck=Pin(18),mosi=Pin(19))
        self.display = st7789.ST7789(self.spi,240,240,dc=Pin(16),rst=Pin(17),cs=Pin(20))
    def fill(self,color):
        self.display.fill(color)
    def pixel(self,start_x,start_y,color):
        self.display.pixel(start_x,start_y, color)
    def line(self,start_x,start_y,end_x,end_y,color):
        self.display.line(start_x,start_y,end_x,end_y ,color)
    def h_line(self,start_x,start_y,length,color):
        self.display.hline(start_x,start_y,length,color)
    def v_line(self,start_x,start_y,length,color):
        self.display.vline(start_x,start_y,length,color)
    def rect(self,start_x,start_y,end_x,end_y,color):
        self.display.fill_rect(start_x,start_y,end_x,end_y ,color)
    def set_display(self):
        self.display.fill(st7789.BLACK)
    def text(self,text,start_x,start_y,color,text_scale):
        self.display.text(text,start_x,start_y,color,scale=text_scale)
class Button():
    def __init__(self):
        self.button_1 = Pin(15, Pin.IN, Pin.PULL_UP)
        self.button_2 = Pin(14, Pin.IN, Pin.PULL_UP)
    def r_push(self):
        if self.button_1.value() == 0:
            flug=True
        else:
            flug=False
        return flug
    def l_push(self):
        if self.button_2.value() == 0:
            flug=True
        else:
            flug=False
        return flug
    def reset_btn():
        #if self.button_reset.value() == 0:
        #    flug=False
        #time.sleep(0.1)
        #return flug
        print("a")