import math
import random

#class Water:{{{1
class Water:
    #def __init__ (self, current): {{{2
    def __init__ (self, current):
        self.speed = 0.0
        self.sediment = 0.0
        self.capacity = 0.0
        self.current = current
        self.previous = None
        self.next = None
        self.evaporate = False

    #def get_evaporate (self): {{{2
    def get_evaporate (self):
        return self.evaporate

    #def update (self): {{{2
    def update (self):
        self.find_next()
        self.calc_speed()
        self.calc_capacity()

        if self.current == self.next:
            if self.sediment < 1:
                self.current.deposit(self.sediment)
                self.sediment = 0.0
                if self.speed < 0.35:
                    self.evaporate = True
            else:
                self.current.deposit(self.sediment / 2.0)
                self.sediment /= 2.0
        else:
            if self.sediment > self.capacity:
                self.current.deposit (self.sediment - self.capacity)
                self.sediment = self.capacity
            elif self.sediment < self.capacity:
                gain_potential = self.capacity - self.sediment
                gain = self.current.erode (gain_potential)
                self.sediment += gain

            self.move()

    #def find_next (self): {{{2
    def find_next (self):
        self.next = self.current.find_next (self.previous)

    #def calc_speed (self): {{{2
    def calc_speed (self):
        h1 = self.current.get_height()
        if self.next == None:
            h2 = h1
        else:
            h2 = self.next.get_height()
        difference = h1 - h2
        temp_speed = (self.speed + difference) / 2.0
        if temp_speed < 0.0:
            temp_speed = 0.0
        if temp_speed > 25.0:
            temp_speed = 25.0
        self.speed = temp_speed

    #def calc_capacity (self): {{{2
    def calc_capacity (self):
        #self.capacity = math.pow(self.speed, 3.0/2.0)
        #self.capacity = math.pow(self.speed, 2.0)/5.0
        self.capacity = self.speed
        

    #def move (self): {{{2
    def move (self):
        self.previous = self.current
        self.current = self.next
        if self.current == None:
            self.evaporate = True
    # }}}2

#class Dirt: {{{1
class Dirt:
    #def __init__ (self, position, height): {{{2
    def __init__ (self, position, height):
        self.position = position
        self.height = height
        self.left = None
        self.right = None

    #def get_height (self): {{{2
    def get_height (self):
        return self.height

    #def get_position (self): {{{2
    def get_position (self):
        return self.position

    #def set_left (self, left): {{{2
    def set_left (self, left):
        self.left = left

    #def set_right (self, right): {{{2
    def set_right (self, right):
        self.right = right

    #def find_next (self, previous): {{{2
    def find_next (self, previous):
        lowest = None
        border = False
        for neighbor in self.left, self.right:
            if neighbor == None:
                border = True
            elif lowest == None:
                lowest = neighbor
            elif neighbor.get_height() < lowest.get_height():
                lowest = neighbor
        if self.height < lowest.get_height():
            if border:
                return None
            else:
                return self
        else:
            return lowest
    
    #def deposit (self, sediment): {{{2
    def deposit (self, sediment):
        self.height += sediment

    #def erode (self, erosion_potential): {{{2
    def erode (self, erosion_potential):
        sediment = (1 + random.random()) * erosion_potential / 2.0
        self.height -= sediment
        return sediment

    #def uplift (self, lift): {{{2
    def uplift (self, lift):
        self.height += lift

    #def update (self): {{{2
    def update (self):
        pass
#}}}1
