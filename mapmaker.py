import sys
import pygame
from pygame.locals import *
import random
import math

class Water:
    def __init__ (self, current):
        self.speed = 0.0
        self.sediment = 0.0
        self.capacity = 0.0
        self.current = current
        self.previous = None
        self.next = None
        self.evaporate = False

    def get_evaporate (self):
        return self.evaporate

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

    def find_next (self):
        self.next = self.current.find_next (self.previous)

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

    def calc_capacity (self):
        #self.capacity = math.pow(self.speed, 3.0/2.0)
        #self.capacity = math.pow(self.speed, 2.0)/5.0
        #self.capacity = self.speed * 5.0
        self.capacity = self.speed
        

    def move (self):
        self.previous = self.current
        self.current = self.next
        if self.current == None:
            self.evaporate = True
        

class Dirt:
    def __init__ (self, position, height):
        self.position = position
        self.height = height
        self.left = None
        self.right = None

    def get_height (self):
        return self.height

    def get_position (self):
        return self.position

    def set_left (self, left):
        self.left = left

    def set_right (self, right):
        self.right = right

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
    
    def deposit (self, sediment):
        self.height += sediment

    def erode (self, erosion_potential):
        #left_height = self.height
        #right_height = self.height
        #if not self.left == None:
            #left_height = self.left.get_height()
        ##if not self.right == None:
            #right_height = self.right.get_height()
        #dif_left = self.height - left_height
        ##dif_right = self.height - right_height
        #digging = 0.0

        sediment = (1 + random.random()) * erosion_potential / 2.0

        #if dif_left > dif_right and dif_left < sediment:
            #digging = sediment - dif_left
        #elif dif_left < dif_right and dif_right < sediment:
            ##digging = sediment - dif_right

        #sediment -= digging * .9

        self.height -= sediment
        return sediment

    def uplift (self, lift):
        self.height += lift

    def update (self):
        pass


if __name__ == "__main__":
    pygame.init()

    n = 700
    dirt_width = 1

    size = n*dirt_width, 700
    screen = pygame.display.set_mode (size)

    # Special user actions class.
    class ActOfNature:
        # def __init__ (self, start_phrase='', end_phrase=''): {{{2
        def __init__ (self, start_phrase='', end_phrase=''):
            self.start_phrase = start_phrase
            self.end_phrase = end_phrase
            self.on = False
            self.cycles = 0
            self.x = 0
            self.y = 0

        # def set_pos (self, (x,y)): {{{2
        def set_pos (self, (x,y)):
            self.x = int(x)
            self.y = int(y)

        # def end (self): {{{2
        def end (self):
            self.on = False
            self.cycles = 0
            self.x = 0
            self.y = 0
            if not self.end_phrase == '':
                print self.end_phrase
        # def start (self, pos=(0,0)): {{{2
        def start (self, pos=(0,0)):
            self.on = True
            self.x, self.y = pos
            if not self.start_phrase == '':
                print self.start_phrase
        # def toggle (self, pos=(0,0)): {{{2
        def toggle (self, pos=(0,0)):
            if self.on:
                self.end()
            else:
                self.start(pos)
        # def update (self, rate): {{{2
        def update (self, rate):
            if self.on:
                self.cycles += 1
                if self.cycles % rate == 0:
                    return True
            return False
        #}}}2

    monsoon = ActOfNature('monsoon starting', 'monsoon ending')
    local_rain = ActOfNature()
    local_uplift = ActOfNature()
    earthquake = ActOfNature('Earthquake!')

    # Set up initial objects and containers.
    profile = []
    for i in range(n):
        if 0 == i:
            height = random.random() * 100.0 + 350
            profile.append(Dirt(i, height))
        else:
            height = random.uniform(-1.0, 1.0) * 20.0 + profile[i-1].get_height()
            #height = random.uniform(-0.5, 1.0) * 20.0 + profile[i-1].get_height()
            profile.append(Dirt (i, height))
            profile[i].set_left(profile[i-1])
            profile[i-1].set_right(profile[i])
    waters = []

    while True:
        screen.fill ((140, 196, 199))
        # Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if event.key == pygame.K_w:
                    monsoon.toggle()
                if event.key == pygame.K_e:
                    earthquake.toggle()

            if  event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    local_rain.start(event.pos)
                if event.button == 3:
                    local_uplift.start(event.pos)

            if event.type == pygame.MOUSEMOTION:
                for local in local_rain, local_uplift:
                    if local.on:
                        local.set_pos(event.pos)
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    local_rain.end()
                if event.button == 3:
                    local_uplift.end()

        # React to input states.
        if monsoon.update(1):
            location = random.randint(0, n-1)
            waters.append (Water(profile[location]))
        if local_rain.update(2):
            x = local_rain.x
            x += int(random.uniform(-0.5, 0.5) * dirt_width * n * .05)
            if 0 <= x and x <= screen.get_width():
                location = (x - (x % dirt_width)) / dirt_width
                waters.append (Water(profile[location]))
        if local_uplift.update(1):
            x = local_uplift.x
            x += int(random.triangular(-0.5, 0.5, 0) * dirt_width * n * .05)
            if 0 <= x and x <= screen.get_width():
                location = (x - (x % dirt_width)) / dirt_width
                for k in range(5):
                    if 0 <= location + k-2 and location + k-2 <= n-1:
                        profile[location + k-2].uplift(2.0 + k)
        if earthquake.update(1):
            for dirt in profile:
                for adjacent in dirt.left, dirt.right:
                    if not adjacent == None:
                        dif = dirt.get_height() - adjacent.get_height()
                        for critical_value in 10.0, 5.0, 3.0, 2.0, 1.0:
                            if math.fabs(dif) > critical_value:
                                if critical_value / 20.0 > random.random():
                                    change = (random.random() + 1) * dif / 4.0
                                    dirt.deposit(-change)
                                    adjacent.deposit(change)
                                break
            if earthquake.cycles >= 3:
                earthquake.end()

        # Update objects
        for water in waters:
            water.update()
            if water.get_evaporate():
                waters.remove (water)
        for dirt in profile:
            dirt.update()

        # Drawing objects. Purposefully separate from update loops.
        for dirt in profile:
            height = dirt.get_height()
            top_coor = size[1] - height
            left_coor = dirt.get_position() * dirt_width
            pygame.draw.rect (screen, (0,137,64), (left_coor, top_coor, dirt_width, height))
        if 1:
            for water in waters:
                radius = 4
                y = int(size[1] - water.current.get_height())
                x = int((water.current.get_position()*1.0 + 0.5) * dirt_width)
                height = water.current.get_height()
                #pygame.draw.circle(screen, (0,70,255), (x,y), radius)
                pygame.draw.circle(screen, (223,39,78), (x,y), radius)


        pygame.display.flip()
        pygame.time.wait(10)
