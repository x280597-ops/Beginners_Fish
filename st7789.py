from machine import Pin, SPI
import time


# =========================================================
# RGB565
# =========================================================

def color565(r, g, b):
    return (
        ((r & 0xf8) << 8) |
        ((g & 0xfc) << 3) |
        (b >> 3)
    )


BLACK = color565(0, 0, 0)
WHITE = color565(255, 255, 255)
RED   = color565(255, 0, 0)
GREEN = color565(0, 255, 0)
BLUE  = color565(0, 0, 255)


# =========================================================
# 5x7 ASCII FONT
# =========================================================

FONT = {
    "A": [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "B": [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
    "C": [0x0F, 0x10, 0x10, 0x10, 0x10, 0x10, 0x0F],
    "D": [0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E],
    "E": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
    "F": [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
    "G": [0x0F, 0x10, 0x10, 0x17, 0x11, 0x11, 0x0F],
    "H": [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    "I": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x1F],
    "J": [0x01, 0x01, 0x01, 0x01, 0x11, 0x11, 0x0E],
    "K": [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
    "L": [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
    "M": [0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11],
    "N": [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
    "O": [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "P": [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
    "Q": [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
    "R": [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
    "S": [0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E],
    "T": [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    "U": [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    "V": [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
    "W": [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
    "X": [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
    "Y": [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
    "Z": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],

    "0": [0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E],
    "1": [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
    "2": [0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F],
    "3": [0x1E, 0x01, 0x01, 0x0E, 0x01, 0x01, 0x1E],
    "4": [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
    "5": [0x1F, 0x10, 0x10, 0x1E, 0x01, 0x01, 0x1E],
    "6": [0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E],
    "7": [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
    "8": [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
    "9": [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C],

    " ": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],

    ".": [0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06],
    ",": [0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x04],
    ":": [0x00, 0x06, 0x06, 0x00, 0x06, 0x06, 0x00],
    "!": [0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04],
    "?": [0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04],
    "-": [0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00],
    "_": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F],
    "+": [0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00],
    "/": [0x01, 0x02, 0x04, 0x08, 0x10, 0x00, 0x00],
}


# =========================================================
# ST7789
# =========================================================

class ST7789:

    def __init__(
        self,
        spi,
        width,
        height,
        dc,
        rst,
        cs=None
    ):

        self.spi = spi
        self.width = width
        self.height = height

        self.dc = dc
        self.rst = rst
        self.cs = cs

        self.dc.init(Pin.OUT, value=0)
        self.rst.init(Pin.OUT, value=1)

        if self.cs is not None:
            self.cs.init(Pin.OUT, value=1)

        self.init()

    # -----------------------------------------------------
    # SPI
    # -----------------------------------------------------

    def _select(self):
        if self.cs is not None:
            self.cs.value(0)

    def _deselect(self):
        if self.cs is not None:
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

    # -----------------------------------------------------
    # Reset
    # -----------------------------------------------------

    def reset(self):

        self.rst.value(1)
        time.sleep_ms(50)

        self.rst.value(0)
        time.sleep_ms(50)

        self.rst.value(1)
        time.sleep_ms(150)

    # -----------------------------------------------------
    # Initialization
    # -----------------------------------------------------

    def init(self):

        self.reset()

        self.write_cmd(0x01)
        time.sleep_ms(150)

        self.write_cmd(0x11)
        time.sleep_ms(120)

        self.write_cmd(0x3A)
        self.write_data(b'\x55')

        self.write_cmd(0x36)
        self.write_data(b'\x00')

        self.write_cmd(0x21)

        self.write_cmd(0x13)

        self.write_cmd(0x29)
        time.sleep_ms(100)

    # -----------------------------------------------------
    # Drawing window
    # -----------------------------------------------------

    def set_window(self, x0, y0, x1, y1):

        self.write_cmd(0x2A)

        self.write_data(bytes([
            x0 >> 8,
            x0 & 0xff,
            x1 >> 8,
            x1 & 0xff
        ]))

        self.write_cmd(0x2B)

        self.write_data(bytes([
            y0 >> 8,
            y0 & 0xff,
            y1 >> 8,
            y1 & 0xff
        ]))

        self.write_cmd(0x2C)

    # -----------------------------------------------------
    # Pixel
    # -----------------------------------------------------

    def pixel(self, x, y, color):

        if x < 0 or x >= self.width:
            return

        if y < 0 or y >= self.height:
            return

        self.set_window(x, y, x, y)

        self.write_data(bytes([
            color >> 8,
            color & 0xff
        ]))

    # -----------------------------------------------------
    # Fill
    # -----------------------------------------------------

    def fill(self, color):

        self.set_window(
            0,
            0,
            self.width - 1,
            self.height - 1
        )

        hi = color >> 8
        lo = color & 0xff

        chunk = bytes([hi, lo]) * 256

        total = self.width * self.height

        self._select()

        self.dc.value(1)

        while total > 0:

            count = min(total, 256)

            self.spi.write(chunk[:count * 2])

            total -= count

        self._deselect()

    # -----------------------------------------------------
    # Filled rectangle
    # -----------------------------------------------------

    def fill_rect(self, x, y, width, height, color):

        if width <= 0 or height <= 0:
            return

        if x < 0:
            width += x
            x = 0

        if y < 0:
            height += y
            y = 0

        if x + width > self.width:
            width = self.width - x

        if y + height > self.height:
            height = self.height - y

        if width <= 0 or height <= 0:
            return

        self.set_window(
            x,
            y,
            x + width - 1,
            y + height - 1
        )

        hi = color >> 8
        lo = color & 0xff

        chunk = bytes([hi, lo]) * 256

        total = width * height

        self._select()

        self.dc.value(1)

        while total > 0:

            count = min(total, 256)

            self.spi.write(chunk[:count * 2])

            total -= count

        self._deselect()

    # -----------------------------------------------------
    # Rectangle
    # -----------------------------------------------------

    def rect(self, x, y, width, height, color):

        self.hline(x, y, width, color)
        self.hline(x, y + height - 1, width, color)

        self.vline(x, y, height, color)
        self.vline(x + width - 1, y, height, color)

    # -----------------------------------------------------
    # Horizontal line
    # -----------------------------------------------------

    def hline(self, x, y, length, color):

        self.fill_rect(
            x,
            y,
            length,
            1,
            color
        )

    # -----------------------------------------------------
    # Vertical line
    # -----------------------------------------------------

    def vline(self, x, y, length, color):

        self.fill_rect(
            x,
            y,
            1,
            length,
            color
        )

    # -----------------------------------------------------
    # Line
    # -----------------------------------------------------

    def line(self, x0, y0, x1, y1, color):

        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1

        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1

        error = dx + dy

        while True:

            self.pixel(x0, y0, color)

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * error

            if e2 >= dy:
                error += dy
                x0 += sx

            if e2 <= dx:
                error += dx
                y0 += sy

    # -----------------------------------------------------
    # Character
    # -----------------------------------------------------

    def char(
        self,
        char,
        x,
        y,
        color,
        scale=1,
        background=None
    ):

        char = char.upper()

        if char not in FONT:
            char = "?"

        data = FONT[char]

        for row in range(7):

            bits = data[row]

            for col in range(5):

                if bits & (1 << (4 - col)):

                    self.fill_rect(
                        x + col * scale,
                        y + row * scale,
                        scale,
                        scale,
                        color
                    )

                elif background is not None:

                    self.fill_rect(
                        x + col * scale,
                        y + row * scale,
                        scale,
                        scale,
                        background
                    )

    # -----------------------------------------------------
    # Text
    # -----------------------------------------------------

    def text(
        self,
        text,
        x,
        y,
        color,
        scale=1,
        background=None
    ):

        start_x = x

        for char in text:

            if char == "\n":

                x = start_x
                y += 8 * scale

                continue

            self.char(
                char,
                x,
                y,
                color,
                scale,
                background
            )

            x += 6 * scale