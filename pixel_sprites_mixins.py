""" BEHAVIOURS """
class SinglePixel(object):
    def __init__(self, **kwargs):
        length = self.end_location - self.start_location
        if length < 0: length = -length
        if self.tocks is None: self.tocks = length + 1
        if type(self.color[0]) is tuple:
            print("Initializing:  <class 'SinglePixel'> as Pallette")
            self.type = 'pallette'
        if type(self.color[0]) is int:
            print("Initializing:  <class 'SinglePixel'> as Mono")
            self.type = 'mono'
    def update_sprite(self):
        if self.tock != self.last_tock:
            self.release_pixel(self.location, mod=self.tail)
            if self.type == 'pallette': self.set_pixel(self.location, self.color[self.location])
            if self.type == 'mono': self.set_pixel(self.location, self.color)
            self.loc_inc()
        return True

class SingleWave(object):
    def __init__(self, **kwargs):
        length = self.end_location - self.start_location
        if length < 0: length = -length
        if self.tocks is None: self.tocks = length + 4 # add splay here, gonna be weird with odd/even splay
    def update_sprite(self):
        self.set_pixel(self.location, self.color[self.tick], mod=self.nose)
        self.set_pixel(self.location, self.color[-1])
        self.set_pixel(self.location, self.color[self.ticks - self.tick], mod=self.tail)
        if self.tock != self.last_tock:
            self.release_pixel(self.location, mod=self.tail)
            self.loc_inc()
        return True

"""Directions"""
class Plus(object):
    def __init__(self, **kwargs):
        if kwargs['start_location'] is None: self.start_location = 0
        else: self.start_location = kwargs['start_location']
        if kwargs['end_location'] is None: self.end_location = len(self.page) - 1
        else: self.end_location = kwargs['end_location']
        self.location = self.start_location
        self.nose = 1
        self.tail = -1
    def set_pixel(self, location, color, mod=0):
        location += mod
        if self.end_location >= location and self.start_location <= location: self.page[location] = color
    def release_pixel(self, location, mod=0):
        location += mod
        if self.end_location >= location and self.start_location <= location: self.page[location] = 0
    def loc_inc(self):
        self.location += 1
    def done(self):
        if self.location > self.end_location: self.end(); return True
class Minus(object):
    def __init__(self, **kwargs):
        if kwargs['start_location'] is None: self.start_location = len(self.page) - 1
        else: self.start_location = kwargs['start_location']
        if kwargs['end_location'] is None: self.end_location = 0
        else: self.end_location = kwargs['end_location']
        self.location = self.start_location
        self.nose = -1
        self.tail = 1
    def set_pixel(self, location, color, mod=0):
        location += mod
        if self.end_location <= location and self.start_location >= location: self.page[location] = color
    def release_pixel(self, location, mod=0):
        location += mod
        if self.end_location <= location and self.start_location >= location: self.page[location] = 0
    def loc_inc(self):
        self.location -= 1
    def done(self):
        if self.location < self.end_location: self.end(); return True
class MirrorIn(object):
    def __init__(self, **kwargs):
        self.start_location = 0
        self.start_location_ = len(self.page)-1
        self.end_location_ = int(len(self.page)/2)
        self.end_location = int(len(self.page)/2) - 1
        self.location = self.start_location
        self.location_ = self.start_location_
        self.nose = 1
        self.tail = -1
    def set_pixel(self, location, color, mod=0):
        location += mod
        location_ = self.location_ - mod
        if self.end_location >= location and self.start_location <= location:
            self.page[location] = color
        if self.end_location_ <= location_ and self.start_location_ >= location_:
            self.page[location_] = color
    def release_pixel(self, location, mod=0):
        location += mod
        location_ = self.location_ - mod
        if self.end_location >= location and self.start_location <= location:
            self.page[location] = 0
        if self.end_location_ <= location_ and self.start_location_ >= location_:
            self.page[location_] = 0
    def loc_inc(self):
        self.location += 1
        self.location_ -= 1
    def done(self):
        if self.location > self.end_location: self.end(); return True
class MirrorOut(object):
    def __init__(self, **kwargs):
        self.start_location = int(len(self.page)/2) - 1
        self.start_location_ = int(len(self.page)/2)
        self.end_location_ = len(self.page)-1
        self.end_location = 0
        self.location = self.start_location
        self.location_ = self.start_location_
        self.nose = -1
        self.tail = 1
        print("start:{},end:{},start_:{},end_:{}".format(self.start_location, self.end_location, self.start_location_, self.end_location_))
    def set_pixel(self, location, color, mod=0):
        location += mod
        location_ = self.location_ - mod
        if self.end_location <= location and self.start_location >= location:
            self.page[location] = color
        if self.end_location_ >= location_ and self.start_location_ <= location_:
            self.page[location_] = color
    def release_pixel(self, location, mod=0):
        location += mod
        location_ = self.location_ - mod
        if self.end_location <= location and self.start_location >= location:
            self.page[location] = 0
        if self.end_location_ >= location_ and self.start_location_ <= location_:
            self.page[location_] = 0
    def loc_inc(self):
        self.location -= 1
        self.location_ += 1
    def done(self):
        if self.location < self.end_location: self.end(); return True
""" RESOLVING FUNCTIONS """
class Terminate(object):
    def __init__(self, **kwargs):
        pass
    def resolve_self(self):
            if self.debugging: print("TERMINATING: ", self, "\n\n")

class Rebound(Terminate): # add echo functionality here and repeat ergo each pass echo -=1
    def __init__(self, **kwargs):
        pass
    def resolve_self(self):
        if self.debugging:
            print("Trying to resolve-Rebound: ")
            for each in self.variables:
                print(each, " :: ", self.variables[each])
        self.variables['start_location'] = self.end_location
        self.variables['end_location'] = self.start_location
        if Plus in type(self).__bases__: self.variables['direction'] = Minus
        if Minus in type(self).__bases__: self.variables['direction'] = Plus
        if self.debugging:
            for each in self.variables:
                print(each, self.variables[each])
        super().resolve_self()
        return self.variables

class Repeat(Terminate):
    def __init__(self, **kwargs):
        pass
    def resolve_self(self):
        if self.debugging:
            print("Trying to resolve-Repeat: ")
            for each in self.variables:
                print(each, " :: ", self.variables[each])
        super().resolve_self()
        return self.variables