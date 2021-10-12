# CircuitPython-Libraries
## hacked_debouncer.py 
Branch from https://github.com/adafruit/Adafruit_CircuitPython_Debouncer
Adds cleaner initialization of buttons/switches by simply passing the board.* object and initializes it as a pull.up input
Adds tracking of consecuitive button presses both short and long

## pixel_sprites.py
Module for advanced abstraction of neopixel patterns.
Class Page wraps https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel 
adds queue based non-blocking timing feature
Class Sprite allows for complex patterns to be built with layers using simple commands such as start here, move there, take this long, do this when done

## pixel_sprites_mixins.py
library of inheritance options for Sprites
includes directions (plus, minus) behaviours (single pixel, pixel wave) and resolutions (rebound, repeat, terminate)

## color_pallette.py
simple implimentation to create rgb/rgbw arrays of tuples
