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
        colSel = pygame.surface(colony.SIZE,pygame.SRCALPHA)
        colSel.circle = pygame.draw.circle(self.screen,colour["2"],self.pos,colony.SIZE[0])
        if self.state == colony.SELLECT:
            colSel.set_alpha(128)
            
        elif self.state == colony.UNACTIVE: #maybe else instead
            colSel.set_alpha(0)
        self.screen.blit(colimage,self.pos)
        self.screen.blit(colSel,self.pos)  
        self.healthdis()
            
            
    def healthcheck(self):
        if self.health >= 50:
            return colour["h1"]
        else
            return colour["h2"]
        
    def healthdis(self):
        #aim is to display the health bar
        ocnum = len(self.inhab) # this is the number of inhabitabts
        healthbg = pygame.surface((colony.SIZE-4)*2, 10),pygame.SRCALPHA)
        healthbg.fill(colour["ht"])
        healthbar = pygame.surface(((((colony.SIZE*2)/100)*self.health), 9),pygame.SRCALPHA)
        healthbar.fill(self.healthcheck())
        font = pygame.font.Font(None,30)
        text_suf = font.render(str(ocnum), 1, colour["ht"])
        tex_pos = (self.pos[0]-colony.SIZE/4,self.pos[1]-colony.SIZE)
        
        #writes to screen
        self.screen.blit(text_suf,tex_pos)
        self.screen.blit(healthbg,(self.pos[0]-colony.SIZE,self.pos[1]+5))
        self.screen.blit(healthbar,(self.pos[0]-colony.SIZE,self.pos[1]+5))
        
        
    def update(self ,time_passed):
        if self.state == colony.SELLECT:
            colsurf = pygame.image.load(self.base_image).convert()
            colsurf.set_alpha(50)
            self.screen.blit(colsurf,(self.pos))
            
            
    def antenter(self,ant)
        if self.owner == ant.owner:
            
        if len(self.inhab) > 0:
            del self.inhab[0]
        else:
            self.health -= value
        
        self.healthdis()
        if self.health == 0:
            self.owner = 0
            self.health = 100
            
    def inhabit(self,ant):
        if self.owner == ant.owner:
            if self.health < 100:
                self.health += 1
                ant.die() # hopefully kill the ant
            else:
                self.inhab.append(ant) # hopefully add the ant to the list
        else:
            if self.health == 0:
                self.owner = ant.owner