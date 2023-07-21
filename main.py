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

# https://learn.adafruit.com/circuitpython-essentials/circuitpython-pins-and-modules
# import microcontroller
# import board
# board_pins = []
# for pin in dir(microcontroller.pin):
#     if isinstance(getattr(microcontroller.pin, pin), microcontroller.Pin):
#         pins = []
#         for alias in dir(board):
#             if getattr(board, alias) is getattr(microcontroller.pin, pin):
#                 pins.append("board.{}".format(alias))
#         if len(pins) > 0:
#             board_pins.append(" ".join(pins))
# for pins in sorted(board_pins):
#     print(pins)


# 1.3" OLED display GME12864-82
# 128x64 white, SH1106 controller
# Similar to https://www.aliexpress.com/item/3256801425708937.html
#   1 GND -
#   2 VDD -
#   3 SCK - SPI ClocK
#   4 SDA - SPI submodule in              I2C Data (Serial Data)
#   5 RES - Reset
#   6 DC  - Command
#   7 CS  - Chip Select

COLSTART1 = 2
WIDTH1 = 128
HEIGHT1 = 64
BORDER1 = 1

# https://www.wemos.cc/en/latest/d1_mini_shield/oled_0_66.html
# 64×48 pixels OLED Shield
# Driver IC: SSD1306 (I2C Address: 0x3C or 0x3D)
COLSTART2 = 32
WIDTH2 = 64
HEIGHT2 = 48
BORDER2 = 1

USE_DISPLAY1 = True
USE_DISPLAY2 = True

if USE_DISPLAY1:
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
    display1 = adafruit_displayio_sh1106.SH1106(display_bus1, width=WIDTH1, height=HEIGHT1, colstart=COLSTART1, brightness=.5)

    # Make the display context
    splash1 = displayio.Group()

    display1.show(splash1)

    color_bitmap = displayio.Bitmap(WIDTH1, HEIGHT1, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash1.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(WIDTH1 - BORDER1 * 2, HEIGHT1 - BORDER1 * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=BORDER1, y=BORDER1
    )
    splash1.append(inner_sprite)

    # Draw a label
    text = "This is not\na chew toy."
    text_area = label.Label(
        terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT1 // 2 - 1
    )
    splash1.append(text_area)

    time.sleep(.5)
    spi.deinit()

if USE_DISPLAY2:
    displayio.release_displays()
    i2c = busio.I2C(board.SCL, board.SDA)
    display_bus2 = displayio.I2CDisplay(i2c, device_address=0x3c)
    display2 = adafruit_displayio_ssd1306.SSD1306(display_bus2, width=WIDTH2, height=HEIGHT2, colstart=COLSTART2)

    # Make the display context
    splash2 = displayio.Group()

    display2.show(splash2)

    color_bitmap = displayio.Bitmap(WIDTH2, HEIGHT2, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash2.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(WIDTH2 - BORDER2 * 2, HEIGHT2 - BORDER2 * 2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=BORDER2, y=BORDER2
    )
    splash2.append(inner_sprite)

    # Draw a label
    text = "This is a\nchew toy."
    text_area = label.Label(
        terminalio.FONT, text=text, color=0xFFFFFF, x=6, y=HEIGHT1 // 4 - 1
    )
    splash2.append(text_area)

    time.sleep(.5)
    i2c.deinit()


pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)

button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

# https://learn.adafruit.com/adafruit-qt-py-esp32-s2/pinouts
# A2, A3, SDA, SCL, TX
#a2 = touchio.TouchIn(board.A2)
a3 = touchio.TouchIn(board.A3)
#sda = touchio.TouchIn(board.SDA)
#scl = touchio.TouchIn(board.SCL)
tx = touchio.TouchIn(board.TX)

v = 0
while True:
    if not button.value:
        pixel.fill((25, 0, 0))
        #print("Click!")
    #elif a2.value:
    #    pixel.fill((0, 25, 0))
    #       #print("Touch A2!")
    elif a3.value:
        pixel.fill((0, 50, 0))
        #print("Touch A3!")
    #elif sda.value:
    #    pixel.fill((0, 100, 0))
    #    #print("Touch SDA!")
    #elif scl.value:
    #    pixel.fill((0, 150, 0))
    #    #print("Touch SCL!")
    elif tx.value:
        pixel.fill((0, 200, 0))
        #print("Touch TX!")
    else:
        pixel.fill((0, 0, v))
        v = 3 - v
        #pixel.fill((random.randint(0,1), random.randint(0,1), random.randint(0,1)))
        time.sleep(.1)

print("End")
