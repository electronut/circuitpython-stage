import board
from micropython import const
import stage
import displayio
import busio
import time
import digitalio
import gamepad
from digitalio import DigitalInOut as do

"""
Buttons:
SW1/A/O           P1.08
SW2/B/X           P1.06
SW3/reset/start   P1.05
SW4/select        P1.04
UP                P0.23
DOWN              P0.26
RIGHT             P0.28
LEFT              P0.21
"""

K_UP = const(0x01)
K_LEFT = const(0x02)
K_DOWN = const(0x04)
K_RIGHT = const(0x08)
K_X = const(0x10)
K_O = const(0x20)
K_SELECT = const(0x40)
K_START = const(0x80)

_TFT_INIT = (
    b"\x01\x80\x80"
    b"\x11\x80\x05"
    b"\x3a\x01\x05"
    b"\x26\x01\x04"
    b"\xf2\x01\x01"
    b"\xe0\x0f\x3f\x25\x1c\x1e\x20\x12\x2a\x90\x24\x11\x00\x00\x00\x00\x00"
    b"\xe1\x0f\x20\x20\x20\x20\x05\x00\x15\xa7\x3d\x18\x25\x2a\x2b\x2b\x3a"
    b"\xb1\x02\x08\x08"
    b"\xb4\x01\x07"
    b"\xc0\x02\x0a\x02"
    b"\xc1\x01\x02"
    b"\xc5\x02\x50\x5b"
    b"\xc7\x01\x40"
    b"\x2a\x04\x00\x00\x00\x7f"
    b"\x2b\x04\x00\x00\x00\x7f"
    b"\x36\x01\xA8"
    b"\x29\x80\x78"
    b"\x2c\x80\x78"
)

class DummyAudio:
    def play(self, f, loop=False):
        pass

    def stop(self):
        pass

    def mute(self, mute):
        pass

tft_cs = board.D4
tft_dc = board.D33
tft_reset = board.D32
tft_SCK=board.D29
tft_MOSI=board.D30
tft_ledk=board.D19

displayio.release_displays()
_tft_spi = busio.SPI(clock=tft_SCK, MOSI=tft_MOSI)
while not _tft_spi.try_lock():
    pass
_tft_spi.configure(baudrate=32000000)
_tft_spi.unlock()

with digitalio.DigitalInOut(tft_reset) as _reset:
    _reset.switch_to_output(value=0)
    time.sleep(0.05)
    _reset.value = 1
    time.sleep(0.05)

_fourwire = displayio.FourWire(_tft_spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset)

display = displayio.Display(_fourwire, _TFT_INIT, width=160, height=128, rotation=0)#, backlight_pin=tft_ledk)
del _TFT_INIT
display.auto_brightness = True

buttons = gamepad.GamePad(do(board.D23), do(board.D21), do(board.D26), do(board.D28), do(board.D38), do(board.D40), do(board.D36), do(board.D37))

audio = stage.Audio(board.D2, board.D31)