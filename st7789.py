from time import sleep_ms


# RGB565変換
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


class ST7789:

    def __init__(self, spi, width, height, dc, rst, cs=None):

        self.spi = spi
        self.width = width
        self.height = height

        self.dc = dc
        self.rst = rst
        self.cs = cs


        self.dc.init(self.dc.OUT)
        self.rst.init(self.rst.OUT)

        if self.cs:
            self.cs.init(self.cs.OUT)


    def _select(self):
        if self.cs:
            self.cs.value(0)


    def _deselect(self):
        if self.cs:
            self.cs.value(1)


    def write_cmd(self, cmd):

        self._select()

        self.dc.value(0)
        self.spi.write(bytes([cmd]))

        self._deselect()


    def write_data(self, data):

        self._select()

        self.dc.value(1)
        self.spi.write(data)

        self._deselect()


    def reset(self):

        self.rst.value(1)
        sleep_ms(50)

        self.rst.value(0)
        sleep_ms(50)

        self.rst.value(1)
        sleep_ms(150)



    def init(self):

        self.reset()


        self.write_cmd(0x01) # SWRESET
        sleep_ms(150)


        self.write_cmd(0x11) # Sleep out
        sleep_ms(120)


        # 色設定
        self.write_cmd(0x3A)
        self.write_data(bytes([0x55])) # RGB565


        # Memory access
        self.write_cmd(0x36)
        self.write_data(bytes([0x00]))


        self.write_cmd(0x21) # inversion on


        self.write_cmd(0x29) # display on

        sleep_ms(100)



    def set_window(self,x0,y0,x1,y1):

        self.write_cmd(0x2A)

        data = bytes([
            x0>>8,x0&255,
            x1>>8,x1&255
        ])

        self.write_data(data)


        self.write_cmd(0x2B)

        data = bytes([
            y0>>8,y0&255,
            y1>>8,y1&255
        ])

        self.write_data(data)


        self.write_cmd(0x2C)



    def pixel(self,x,y,color):

        if x < 0 or y < 0:
            return

        if x >= self.width or y >= self.height:
            return


        self.set_window(x,y,x,y)

        self.write_data(bytes([
            color >> 8,
            color & 0xff
        ]))



    def fill(self,color):

        self.fill_rect(
            0,
            0,
            self.width,
            self.height,
            color
        )



    def fill_rect(self,x,y,w,h,color):

        self.set_window(
            x,
            y,
            x+w-1,
            y+h-1
        )


        high = color >> 8
        low = color & 0xff


        data = bytes([high,low]) * (w*h)

        self.write_data(data)



    def line(self,x0,y0,x1,y1,color):

        dx = abs(x1-x0)
        dy = abs(y1-y0)

        sx = 1 if x0<x1 else -1
        sy = 1 if y0<y1 else -1

        err = dx-dy


        while True:

            self.pixel(x0,y0,color)

            if x0==x1 and y0==y1:
                break


            e2=2*err

            if e2>-dy:
                err-=dy
                x0+=sx

            if e2<dx:
                err+=dx
                y0+=sy