#!/usr/bin/env python

import sys
import math, random

import pygame
from pygame.locals import *

import nature, options
from terrain import Dirt, Water

pygame.init()

dirt_width = options.dirt_width

size = options.n * dirt_width, 700
screen = pygame.display.set_mode(size)

# Set up initial objects and containers. {{{1
monsoon = nature.ActOfNature('monsoon starting', 'monsoon ending')
local_rain = nature.ActOfNature()
local_uplift = nature.ActOfNature()
earthquake = nature.ActOfNature('Earthquake!')

profile = []
for i in range(options.n):
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
# }}}1

# Main loop {{{1
while True:
    screen.fill ((140, 196, 199))
    # Input {{{2
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

    # React to input states. {{{2
    if monsoon.update(options.monsoon_cycle_rate):
        location = random.randint(0, options.n-1)
        waters.append (Water(profile[location]))
    if local_rain.update(options.local_rain_cycle_rate):
        x = local_rain.x
        x += int(random.triangular(-0.5, 0.5, 0) * dirt_width * options.n * .05)
        if 0 <= x and x <= screen.get_width():
            location = (x - (x % dirt_width)) / dirt_width
            waters.append (Water(profile[location]))
    if local_uplift.update(options.local_uplift_cycle_rate):
        x = local_uplift.x
        x += int(random.triangular(-0.5, 0.5, 0) * dirt_width * options.n * .05)
        if 0 <= x and x <= screen.get_width():
            location = (x - (x % dirt_width)) / dirt_width
            for k in -2, -1, 0, 1, 2:
                if 0 <= location + k and location + k <= options.n-1:
                    profile[location + k].uplift(2.0 + math.fabs(k))
    if earthquake.update(options.earthquake_cycle_rate):
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
        if earthquake.cycles >= options.earthquake_max_cycles:
            earthquake.end()

    # Update objects {{{2
    for water in waters:
        water.update()
        if water.get_evaporate():
            waters.remove (water)
    for dirt in profile:
        dirt.update()

    # Render objects. {{{2
    # Purposefully separate from update loops.
    for dirt in profile:
        height = dirt.get_height()
        top_coor = size[1] - height
        left_coor = dirt.get_position() * dirt_width
        pygame.draw.rect (screen, (0,137,64), (left_coor, top_coor, dirt_width, height))

    if options.render_water:
        for water in waters:
            radius = 4
            y = int(size[1] - water.current.get_height())
            x = int((water.current.get_position()*1.0 + 0.5) * dirt_width)
            height = water.current.get_height()
            #pygame.draw.circle(screen, (0,70,255), (x,y), radius)
            pygame.draw.circle(screen, (223,39,78), (x,y), radius)
    # }}}2


    pygame.display.flip()
    pygame.time.wait(options.main_sleep_time)
# }}}1
