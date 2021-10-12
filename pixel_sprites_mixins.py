""" BEHAVIOURS """
class SinglePixel(object):
    def __init__(self, **kwargs):
        if self.tocks is None: self.tocks = len(self.page)
        if type(self.color[0]) is tuple:
            print("Initializing:  <class 'SinglePixel'> as Pallette")
            self.type = 'pallette'
        if type(self.color[0]) is int:
            print("Initializing:  <class 'SinglePixel'> as Mono")
            self.type = 'mono'
    def update_sprite(self):
        if tock != last_tock:
            self.release_pixel(self.location+self.tail)
            if self.type == 'pallette': self.set_pixel(self.location, self.color[self.location])
            if self.type == 'mono': self.set_pixel(self.location, self.color)
            self.location += self.nose
        return True

class SingleWave(object):
    def __init__(self, **kwargs):
        if self.tocks is None: self.tocks = len(self.page) + 3 # add splay here, gonna be weird with odd/even splay
    def update_sprite(self):
        self.set_pixel(self.location+self.nose, self.color[self.tick])
        if not self.fill: self.set_pixel(self.location+self.tail, self.color[self.ticks - self.tick])
        if self.tock != self.last_tock:
            if not self.fill: self.release_pixel(self.location+self.tail)
            self.location += self.nose
            self.set_pixel(self.location, self.color[-1])
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
    def set_pixel(self, location, color):
        try:
            if self.end_location >= location and self.start_location <= location:
                self.page[location] = color
        except:
            pass
    def release_pixel(self, location):
        try:
            if self.end_location >= location and self.start_location <= location:
                self.page[location] = 0
        except: pass
    def done(self):
        if self.location > self.end_location:
            self.end()
            return True
class Minus(object):
    def __init__(self, **kwargs):
        if kwargs['start_location'] is None: self.start_location = len(self.page) - 1
        else: self.start_location = kwargs['start_location']
        if kwargs['end_location'] is None: self.end_location = 0
        else: self.end_location = kwargs['end_location']
        self.location = self.start_location
        self.nose = -1
        self.tail = 1
    def set_pixel(self, location, color):
        try:
            if self.end_location <= location and self.start_location >= location:
                self.page[location] = color
        except: pass
    def release_pixel(self, location):
        try:
            if self.end_location <= location and self.start_location >= location:
                self.page[location] = 0
        except: pass
    def done(self):
        if self.location < self.end_location:
            self.end()
            return True
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
        Terminate.resolve(self)
        return self.variables

class Repeat(Terminate):
    def __init__(self, **kwargs):
        pass
    def resolve_self(self):
        if self.debugging:
            print("Trying to resolve-Repeat: ")
            for each in self.variables:
                print(each, " :: ", self.variables[each])
        Terminate.resolve(self)
        return self.variables