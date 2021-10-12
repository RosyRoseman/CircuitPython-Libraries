import time
import neopixel
import gc
from pixel_sprites_mixins import *

def build_sprite(direction=Plus, resolve=Terminate, behaviour=None, **kwargs):
    class Sprite(behaviour, direction, resolve,):
        def __init__(self,
                    color=(0,10,10),
                    page=None,
                    start_location=None,
                    end_location=None,
                    priority=0,
                    ticks=9,
                    tocks=None,
                    echo=0,
                    echo_changes={},
                    start_time=time.monotonic(),
                    duration=2,
                    fill=False,
                    splay = 1,
                    debugging=False,
                    **kwargs
                    ):
            self.color = color
            self.page = page
            self.start_location = start_location
            self.end_location = end_location
            self.priority = 0
            self.ticks = ticks
            self.tocks = tocks
            self.tick = 0
            self.tock = 0
            self.last_tick = self.tick
            self.last_tock = self.tock
            self.echo = echo
            self.echo_changes = echo_changes # {'color':[pallette, pallette, pallette], 'duration':[4,2,2]}
            self.start_time = start_time
            self.end_time = start_time + duration
            self.duration = duration
            self.fill = fill
            self.splay = splay
            self.debugging = debugging
            self.direction = direction
            self.resolve = resolve
            self.behaviour = behaviour
            for each in Sprite.__bases__:
                if self.debugging: print("Initializing: ",each)
                each.__init__(self, **self.__dict__)
            self.time = None
            self.delay = self.duration / self.tocks
            self.tick_delay = self.delay / self.ticks
            hodl = {}
            for each in self.__dict__:
                hodl[each] = self.__dict__[each]
            self.variables = hodl
            if self.debugging:
                for each in self.variables:
                    print(each, self.variables[each])
            self.page.init_q(self)
        def update(self):
            if self.tick > self.ticks:
                self.tock +=1
                self.tick = 0
            if self.tock > self.tocks:
                self.resolve_self()
                if self.echo:
                    self.variables['echo'] -=1
                    for each in self.echo_changes:
                        self.variables[each] = self.variables['echo_changes'][each].pop(0)
                    build_sprite(**self.variables)
                return
            self.update_sprite()
            self.page.show()
            self.tick +=1
            self.last_tick = self.tick
            self.last_tock = self.tock
            self.page.update_q(self)
    return Sprite(**kwargs)

""" Page: wrapper for a neopixel object. """
class Page(neopixel.NeoPixel):
    def __str__(self):
        return Page.__bases__[0]
    def __init__(self, pin, n, *, bpp=3, brightness=1.0, auto_write=True, pixel_order=None, background=None, debugging=False):
        self.q = []
        self.now = 0
        self.debugging=debugging
        super().__init__(
            pin, n, bpp=bpp, brightness=brightness, auto_write=auto_write, pixel_order=pixel_order
        )
        if len(self.byteorder) == 3: self.fill((0,0,0))
        if len(self.byteorder) == 4: self.fill((0,0,0,0))
        self.show()
    def init_q(self, sprite):
        sprite.time = time.monotonic()
        self.q.append([sprite.start_time, sprite])
        def func(e): return e[0]
        self.q.sort(key=func)
    def check_q(self):
        now = time.monotonic()
        try:
            if now >= self.q[0][0]:
                active = self.q.pop(0)
                active[1].update()
        except IndexError:
            if self.debugging: print("Q is empty"); time.sleep(.05)
    def update_q(self, sprite):
        now = time.monotonic()
        sprite.time = sprite.time + sprite.tick_delay
        self.q.append([sprite.time, sprite])
        def func(e): return e[0]
        self.q.sort(key=func)
        return self.q
    def release_all_pixels(self, priority=0):
        if self.debugging: print("Releasing all pixels")
        for each in self:
            each = 0
        self.show()