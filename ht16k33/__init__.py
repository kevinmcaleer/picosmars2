"""
Radomir Dopieralski 2016 for Adafruit Industries
Tony DiCola 2016 for Adafruit Industries
Dale Weber 2021

License-Identifier: MIT

- Authors: Radomir Dopieralski & Tony DiCola for Adafruit Industries
- Ported to Micropython by Dale Weber <hybotics.wy@gmail.com>
- Code tidied up, tested and ported to work with standard MicroPython 
  on the Raspberry Pi Pico, added Text scrolling, and icons too

"""

from micropython import const
from time import sleep
from machine import I2C

BLINK_CMD = const(0x80)
BLINK_DISPLAYON = const(0x01)
CMD_BRIGHTNESS = const(0xE0)
OSCILATOR_ON = const(0x21)

from .icons import heart, smile, sad, ghost, small_heart, tick, skull, cross, micropython, happy, neutral, sadface, eyes_closed, wink, oof, sleepy
from .scroller import *

class HT16K33:
    """The base class for all HT16K33-based backpacks and wings."""

    def __init__(self, i2c, address=0x70, auto_write=True, brightness=1.0):
        self.i2c = i2c
        self.i2c_address = address
        self._temp = bytearray(1)
        self._buffer = bytearray(17)
        self._auto_write = auto_write
        self.fill(0)
        self._write_cmd(OSCILATOR_ON)
        self._blink_rate = None
        self._brightness = None
        self.blink_rate = 0
        self.brightness = brightness
        self.fill(0)

    def _write_cmd(self, byte):
        self._temp[0] = byte
        self.i2c.writeto(self.i2c_address,self._temp)

    @property
    def blink_rate(self):
        """The blink rate. Range 0-3."""
        return self._blink_rate

    @blink_rate.setter
    def blink_rate(self, rate=None):
        """ Set the blink rate to one of the predefined rates """
        if not 0 <= rate <= 3:
            raise ValueError("Blink rate must be an integer in the range: 0-3")
        rate = rate & 0x03
        self._blink_rate = rate
        self._write_cmd(BLINK_CMD | BLINK_DISPLAYON | rate << 1)

    @property
    def brightness(self):
        """The brightness. Range 0.0-1.0"""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness:float):
        """ Set the brightness to a value between 0.0 and 1.0"""
        if not 0.0 <= brightness <= 1.0:
            raise ValueError(
                "Brightness must be a decimal number in the range: 0.0-1.0"
            )

        self._brightness = brightness
        led_brightness = round(15 * brightness)
        led_brightness = led_brightness & 0x0F
        self._write_cmd(CMD_BRIGHTNESS | led_brightness)

    @property
    def auto_write(self):
        """Auto write updates to the display."""
        return self._auto_write

    @auto_write.setter
    def auto_write(self, auto_write:bool):
        """ Set auto write to True or False"""
        if isinstance(auto_write, bool):
            self._auto_write = auto_write
        else:
            raise ValueError("Must set to either True or False.")

    def show(self):
        """Refresh the display and show the changes."""
        
        self.i2c.writeto(self.i2c_address, self._buffer)

    def update(self):
        self.show()

    def fill(self, color:int):
        """Fill the whole display with the given color."""
        fill = 0xFF if color else 0x00
        for i in range(16):
            self._buffer[i + 1] = fill
        if self._auto_write:
            self.show()
    def clear(self):
        self.fill(0)

    def reverse_pixel(self, x:int, y:int, color:bool=None):
        """ Draw a pixel on the display """
        x_order = [6,5,4,3,2,1,0,7]
        x = x_order[x]
    
        addr = 2 * y + x // 8
        mask = 1 << x % 8
        
        if color is None:
            return bool(self._buffer[addr] & mask)
        
        if color:
            self._buffer[addr+1] |= mask # set the bit
        else:
            self._buffer[addr+1] &= ~mask # clear the bit

        if self._auto_write:
            self.show()
            
        return None

    def pixel(self, x:int, y:int, color:bool=None):
        """ Draw a pixel on the display """
        x_order = [7, 0, 1, 2, 3, 4, 5, 6]
        x = x_order[x]
    
        addr = 2 * y + x // 8
        mask = 1 << x % 8
        
        if color is None:
            return bool(self._buffer[addr] & mask)
        
        if color:
            self._buffer[addr+1] |= mask # set the bit
        else:
            self._buffer[addr+1] &= ~mask # clear the bit

        if self._auto_write:
            self.show()
            
        return None
    
    def _set_buffer(self, i, value):
        """Set buffer value at position i to value"""
        self._buffer[i+1] = value 

    def _get_buffer(self, i):
        """Get buffer value at position i"""
        return self._buffer[i+1]  
    
    def icon(self, icon_array):
        """Display an icon on the display."""
        for row in range(8):
            for col in range(8):
                bit = (icon_array[row] >> col) & 0b1
                self.pixel(row, col, bit)
        if not self._auto_write:
            self.show()

    def show_icon(self, name):
        """Display an icon on the display."""
        icons = {
            "heart": heart,
            "smile": smile,
            "sad": sad,
            "ghost": ghost,
            "small_heart": small_heart,
            "tick" : tick,
            "skull" : skull,
            "cross" : cross,
            "micropython" : micropython,
            "happy" : happy,
            "neutral" : neutral,
            "sadface" : sadface,
            "eyes_closed" : eyes_closed,
            "wink" : wink,
            "oof" : oof,
            "sleepy": sleepy,
        }

        if name in icons:
            self.icon(icons[name])
        else:
            valid_icons = ", ".join(icons.keys())
            raise ValueError(f"Icon name must be one of: {valid_icons}")

        