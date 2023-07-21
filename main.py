import random
import board
import time
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1106
import adafruit_displayio_ssd1306
import touchio
import digitalio
import neopixel
import adafruit_datetime

print("-------------------------------------BEGIN-------------------------------------")
print(adafruit_datetime.datetime.now().isoformat())
print("-------------------------------------BEGIN-------------------------------------")

# 1.3" OLED display GME12864-82
# 128x64 white, SH1106 controller
# Similar to https://www.aliexpress.com/item/3256801425708937.html
#   1 GND -
#   2 VDD -
#   3 SCK - SPI Clock
#   4 SDA - SPI submodule in              I2C Data (Serial Data)
#   5 RES - Reset
#   6 DC  - Command
#   7 CS  - Chip Select

COLSTART1 = 2
WIDTH = 128
HEIGHT = 64
BORDER = 1

displayio.release_displays()

# https://www.sparkfun.com/spi_signal_names
spi = busio.SPI(board.SCK, board.MOSI)
display_bus1 = displayio.FourWire(
    spi,
    command=board.A0,     # OLED_DC
    chip_select=board.A1, # OLED_CS
    reset=board.A2,       # OLED_RESET
    baudrate=1000000,
)

# https://docs.circuitpython.org/projects/displayio_sh1106/en/latest/
display1 = adafruit_displayio_sh1106.SH1106(display_bus1, width=WIDTH, height=HEIGHT, colstart=COLSTART1, brightness=.5)

# Make the display context
group = displayio.Group()

display1.show(group)

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
group.append(bg_sprite)

# Draw a smaller inner rectangle
inner_bitmap = displayio.Bitmap(WIDTH - BORDER * 2, HEIGHT - BORDER * 2, 1)
inner_palette = displayio.Palette(1)
inner_palette[0] = 0x000000  # Black
inner_sprite = displayio.TileGrid(
    inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
)
group.append(inner_sprite)

# Draw a label
text = "Bounce!"
textlabel = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
)
group.append(textlabel)

ballgroup = displayio.Group()
group.append(ballgroup)

numcolors = 2
palette = displayio.Palette(numcolors)
palette[0] = 0x000000  # Black
palette[1] = 0xffffff  # White

ballsize = 3
ballbitmap = displayio.Bitmap(ballsize, ballsize, numcolors)
for i in range(0, ballsize * ballsize):
    ballbitmap[i] = 1

tilegrid = displayio.TileGrid(ballbitmap, pixel_shader=palette, width=1, height=1, tile_width=ballsize, tile_height=ballsize)
tilegrid[0] = 0
ballgroup.append(tilegrid)

x = float((WIDTH - ballsize) / 2)
y = float((HEIGHT - ballsize) / 2)
dx = 2.0
dy = 1.0
while True:
    x += dx
    y += dy
    if x<0 or x>WIDTH-ballsize:
        dx = -dx
        x += dx
        dx = dx/abs(dx) * (random.random() * 2 + 1)
    if y<0 or y>HEIGHT-ballsize:
        dy = -dy
        y += dy
        dy = dy/abs(dy) * (random.random() * 2 + 1)
    ballgroup.x = round(x)
    ballgroup.y = round(y)
    # print(f"x={x} y={y}")
    time.sleep(.01)

# time.sleep(.5)
# spi.deinit()

# print("End")
