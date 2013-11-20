from __future__ import division
import os, sys
from random import randrange, randint
from math import hypot

import pygame
from pygame import Rect
from pygame.sprite import Sprite

SIZE=(600,600)



colour = {0:pygame.color.THECOLORS["white"],
          1:pygame.color.THECOLORS["red"],
          2:pygame.color.THECOLORS["blue"],
          3:pygame.color.THECOLORS["yellow"],
          "bg":pygame.color.THECOLORS["black"],
          "ht":pygame.color.THECOLORS["grey"],
          "h1":pygame.color.THECOLORS["green"],
          "h2":pygame.color.THECOLORS["red"]
          } # change this bit to images maybe
levels = {"1":"level1.cvs",
          "2":"level2.cvs"}

def mapload():
    ## code here to load up the csv and create the map acordingly
    pass


class colony(Sprite):
    

    
    baseimage = {0:"Colony.png",
                 1:"Colony1.png",
                 2:"Colony2.png",
                 3:"Colony3.png"}
    SIZE=(20,20)
    
    def __init__(self, screen, pos, owner):
        Sprite.__init__(self)
        self.screen = screen
        self.pos = pos
        self.owner = owner
        self.health = 100 # max 100
        self.inhab = []
        self.state = False
        self.show()
        (self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2)
   
    
    
    def healthcheck(self):
        if self.health >= 50:
            return colour["h1"]
        else:
            return colour["h2"]
      
    def __str__(self):
        # returns the information aboself.pos[0]-colony.SIZE[0]/4,ut the col to the computer
        return str(self.owner) + "," + str(self.health) + "," + str(len(self.inhab))  
    
    def show(self):
        colimage = pygame.image.load(colony.baseimage[self.owner]).convert_alpha()
        
        #aim is to display the health bar
        ocnum = len(self.inhab) # this is the number of inhabitabts
        healthbg = pygame.Surface((((colony.SIZE[0]-4)*2), 10),pygame.SRCALPHA)
        healthbg.fill(colour["ht"])
        healthbar = pygame.Surface((((((colony.SIZE[0]-5)*2)/100)*self.health), 7),pygame.SRCALPHA)
        healthbar.fill(self.healthcheck())
        font = pygame.font.Font(None,30)
        text_suf = font.render(str(ocnum), 1, colour["ht"])
        tex_pos = (self.pos[0]+4,self.pos[1]-11)
        
        #writes to screen
        self.screen.blit(colimage,(self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2))
        self.screen.blit(text_suf,tex_pos)
        self.screen.blit(healthbg,(self.pos[0]-6,self.pos[1]+12))
        self.screen.blit(healthbar,((self.pos[0]-5),self.pos[1]+13.5))
       
            
       
            
    def collide(self,ant):
        if self.health == 0:
                self.owner = 010
                self.health = 100
        
        if self.owner == ant.owner:
            if self.health < 100:
                self.health += 1
                ant.die() # hopefully kill the ant
            else:
                self.inhab.append(ant) # hopefully add the ant to the list
        else:         
            if len(self.inhab) > 0:
                del self.inhab[0]
            else:
                self.health -=self.value
            
            if self.health == 0:
                self.owner = ant.owner
                self.health = 0

        
    def update(self ,time_passed):
        self.show()
        #send the data and creates new ants
        if time_passed % 2:
            if self.pos != (0,0):
                if len(self.inhab) > 0:
                    for ant in self.inhab:
                        ant(self.pos)
                        pass
            else:
                #create ant
                pass
            
    def draw_select(self):
        
        sel = pygame.Surface((colony.SIZE[0]*2,colony.SIZE[1]*2))
        if self.state == True:
            ucolour = list(colour[self.owner])
            ucolour[3]=255
            sel.fill(ucolour)
        if self.state == False:
            sel.fill((0,122,49,255))
            
        self.screen.blit(sel,(self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2))
        
    def _mouseClick(self,mouspos):
        if hypot ((self.pos[0]-mouspos[0]),(self.pos[1]-mouspos[1])) <= colony.SIZE[0] :
            print str(self.state)
            if self.owner == 1:
                if self.state == False:
                    self.state = True
                else:
                    self.state = False
                    self.des = mouspos
                self.draw_select()
        else:
            if self.state == True:
                if len(self.inhab) > 0:
                    for ant in self.inhab:
                        ant.set_target(mouspos)

class ant(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        



pygame.init()
ant_tick = 0
col_tick = 0

###### list of all the sprite groups
colony_list = pygame.sprite.Group()
ant_list = pygame.sprite.Group()
#all_sprite_list = pygame.sprite.Group()

#####Screen
window = pygame.display.set_mode(SIZE)
bg_img = pygame.image.load("grass.jpg").convert()
window.blit(bg_img,(0,0,600,600))

#####Produce the map
mapload() ## this will be a funtion to load a file(.csv) and set the colong info to it
for i in range(5):
    col = colony(window,(randrange(20,SIZE[0]-20),randrange(20, SIZE[1]-20)), randint(0,3))
    colony_list.add(col)


clock = pygame.time.Clock()

def stop():    
    pygame.quit()

while True:

    
    pygame.display.update()
    event = pygame.event.poll()
    
    clock.tick()
    elapsed = clock.get_time()

    ant_tick += elapsed
    col_tick += elapsed
    if ant_tick > 25:
        ant_tick = 0
    if col_tick > 1000:
        col_tick = 0    
        
        
    for c in colony_list: 
        c .update(col_tick)
        
           
    if event.type == pygame.QUIT:
        stop()
    if event.type == pygame.MOUSEBUTTONDOWN:
        loc = pygame.mouse.get_pos()
        for c in colony_list:
            c._mouseClick(loc)
 