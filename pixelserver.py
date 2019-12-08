from xmlrpc.server import SimpleXMLRPCServer
import board
import neopixel
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 250

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False,
                           pixel_order=ORDER)


def light_one(index):
    pixels.fill((0,0,0))
    pixels[index] = (255,0,0)
    pixels.show()

def clear():
    pixels.fill((0,0,0))
    pixels.show()


server = SimpleXMLRPCServer(('0.0.0.0',8000), allow_none=True)
server.register_introspection_functions()
server.register_function(light_one)
server.register_function(clear)
server.serve_forever()

