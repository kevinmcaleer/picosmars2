from ht16k33 import HT16K33
from machine import I2C, Pin

id = 0
sda = Pin(0)
scl = Pin(1)
address = 0x70

face = [
    0b01111110,
    0b10000001,
    0b10100101,
    0b10000001,
    0b10100101,
    0b10011001,
    0b10000001,
    0b01111110,
    ]

i2c = I2C(id, sda=sda, scl=scl)
matrix = HT16K33(i2c)

matrix.icon(face)
matrix.show()