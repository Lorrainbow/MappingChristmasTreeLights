#!/usr/bin/python3

import time
import board
import neopixel
import numpy as np
import colorsys
from functools import partial

NUM_PIXELS = 100
SPEED = 0.3

pixel_pin = board.D18
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, NUM_PIXELS, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)

xyz = np.loadtxt('/home/pi/xyz.csv',delimiter=',', skiprows=1).T
rad = np.arctan2(xyz[1],xyz[0])/(np.pi*2)
minh = np.min(xyz[2])
maxh = np.max(xyz[2])
height = 1-(xyz[2] - minh) / (maxh-minh)
start = time.time()


WHITE = np.array((255, 255, 255), dtype='uint8')
BLUE = np.array((0,0,255), dtype='uint8')
GREEN = np.array((0, 255, 0), dtype='uint8')
RED = np.array((255, 0, 0), dtype='uint8')
YELLOW = np.array((0, 255, 255), dtype='uint8')
PURPLE = np.array((255, 0, 255), dtype='uint8')

def fade_in(val, now):
    v = ((val+now*SPEED) % 1) * 4
    if v>1.0:
        v = 2-v
    v = max(v,0)
    v = min(1,v)
    return v    

def wash(val, now):
    v = ((val+now*SPEED) % 1) * 4 -1
    v = max(-v,0)
    v = min(1,v)
    return v

def stripe(func, colour):
    def f(val, now):
        v = func(val, now)
        return tuple(np.array(colour*v,dtype="uint8"))
    return f
    
def rainbow(val, now):
    rgb = colorsys.hsv_to_rgb(val+now*SPEED,1,1)
    return tuple(np.array(tuple(x*255 for x in rgb), dtype="uint8"))




def animate(source, func, forever=False):
    start = time.time()
    while True:
        now = time.time() - start
        for i in range(NUM_PIXELS):
            rgb = func(source[i],now)
            pixels[i] = rgb
        pixels.show()
        if now > 20 and not forever:
            break

vertical = partial(animate, height)
rotate = partial(animate, rad)

while True:
    vertical(rainbow)
    vertical(stripe(fade_in, WHITE))
    rotate(stripe(wash, RED))
    rotate(stripe(wash, BLUE))
    vertical(stripe(fade_in, YELLOW))
    rotate(rainbow)
    rotate(stripe(fade_in,PURPLE))
    vertical(stripe(wash, GREEN))

