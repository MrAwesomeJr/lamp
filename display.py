import neopixel
import board

class Display:
    # deals with the neopixel stuff
    def __init__(self, pin=board.D12, leds=50, pixel_order=neopixel.RGB):
        self.pixels = neopixel.NeoPixel(pin, leds, auto_write=False, pixel_order=pixel_order)

    def __del__(self):
        self.pixels.deinit()

    def show(self, strip, blocking=True):
        pass