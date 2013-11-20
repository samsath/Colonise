from __future__ import division
import os, sys
from random import randint
from math import sin, cos, atan2, degrees, pi, hypot

import pygame
from pygame import Rect
from pygame.sprite import Sprite

SIZE=(600,600)



colour = {"0":pygame.color.THECOLORS["white"],
          "1":pygame.color.THECOLORS["red"],
          "2":pygame.color.THECOLORS["blue"],
          "bg":pygame.color.THECOLORS["black"],
          "ht":pygame.color.THECOLORS["grey"],
          "h1":pygame.color.THECOLORS["green"],
          "h2":pygame.color.THECOLORS["red"]
          } # change this bit to images maybe

class colony(Sprite):
    baseimage = {"0":"colony.png",
                 "1":"colony1.png",
                 "2":"colony2.png"}
    SIZE=(40,40)
    
    def __init__(self, screen, c_image, pos, owner):
        self.screen = screen
        self.pos = pos
        self.owner = owner
        self.health = 100 # max 100
        self.inhab = []
        self.state = colony.SELLECT
        self.show()
        
    def is_sellect(self):
        return self.state in (colony.SELLECT, colony.UNACTIVE)
    
    
    def show(self):
        colimage = pygame.image.load(colony.baseimage[self.owner]).convert()
        if self.state == colony.SELLECT:
            colSel = pygame.surface(colony.SIZE,pygame.SRCALPHA)
            colSel = pygame.draw.circle()
            colSel.set_alpha(128)
            
            
    def update(self,time_passed):
        if self.state == colony.SELLECT:
            colsurf = pygame.image.load(self.base_image).convert()
            colsurf.set_alpha(50)
            self.screen.blit(colsurf,(self.pos))
            