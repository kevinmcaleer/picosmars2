from ht16k33 import HT16K33
from machine import I2C, Pin
from time import sleep
from ht16k33.scroller import Scroller

id = 0
sda = Pin(0)
scl = Pin(1)
address = 0x70

i2c = I2C(id, sda=sda, scl=scl)
matrix = HT16K33(i2c)

def blink(times):
    for _ in range(times):
        matrix.show_icon("happy")
        sleep(0.1)
        matrix.clear()
        matrix.show_icon("eyes_closed")
        sleep(0.1)
        matrix.show_icon("happy")
        sleep(0.1)
        matrix.clear()
    matrix.clear()

def pulse_heart(times):

    for _ in range(times):
        matrix.show_icon("heart")
        sleep(0.1)
        matrix.clear()
        matrix.show_icon("small_heart")
        sleep(0.1)
        matrix.clear()
    matrix.clear()



def show_message(message):
    scroll.num_cols = 8
    scroll.num_rows = 5
    for position in range(0, -len(message*(scroll.num_cols)), -1):

        matrix.clear()
        matrix.auto_write = False
        scroll.show_message(message, position)
        matrix.update()
        sleep(0.05)

def demo():
    matrix.show_icon("happy")
    sleep(1)
    blink(2)
    sleep(1)
    matrix.show_icon("oof")
    sleep(1)

    pulse_heart(10)
    
    message = '    Hey Robot Makers!'

    show_message(message)

scroll = Scroller(matrix)
while True:
    matrix.show_icon("happy")
#     demo()