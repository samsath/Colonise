from __future__ import division
import os, sys
from random import randrange
from math import hypot

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
levels = {"1":"level1.cvs",
          "2":"level2.cvs"}

def mapload():
    ## code here to load up the csv and create the map acordingly
    pass


class colony(Sprite):
    
    (SELLECT, UNACTIVE) = range(2)
    
    baseimage = {"0":"Colony.png",
                 "1":"Colony1.png",
                 "2":"Colony2.png"}
    SIZE=(20,20)
    
    def __init__(self, screen, pos, owner):
        Sprite.__init__(self)
        self.screen = screen
        self.pos = pos
        self.owner = str(owner)
        self.health = 100 # max 100
        self.inhab = ["a1","a2","a3","a4","a5"]
        self.state = colony.SELLECT
        self.show()
        
    def is_sellect(self):
        return self.state in (colony.SELLECT, colony.UNACTIVE)
    
    
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
        colSel = pygame.Surface(colony.SIZE,pygame.SRCALPHA)
        pygame.draw.ellipse(colSel,colour[self.owner],[self.pos,colony.SIZE])
        #colSel.circle = pygame.draw.circle(self.screen,colour["2"],self.pos,colony.SIZE[0])
        if self.state == colony.SELLECT:
            colSel.set_alpha(128)
            
        elif self.state == colony.UNACTIVE: #maybe else instead
            colSel.set_alpha(0)
        #self.screen.blit(colimage,(self.pos[0]/2,self.pos[1]/2))
        self.screen.blit(colimage,(self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2))
        self.screen.blit(colSel,(self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2))  
        
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
        self.screen.blit(text_suf,tex_pos)
        self.screen.blit(healthbg,(self.pos[0]-6,self.pos[1]+12))
        self.screen.blit(healthbar,((self.pos[0]-5),self.pos[1]+13.5))
       
            
       
            
    def collide(self,ant):
        if self.health == 0:
                self.owner = 0
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
                for ant in self.inhab:
                    #ant(self.pos)
                    pass
            else:
                #create ant
                pass
   
    def _mouseClick(self,mouspos):
        if hypot ((self.pos[0]-mouspos[0]),(self.pos[1]-mouspos[1])) <= colony.SIZE[0] :
            
            if self.state == colony.UNACTIVE:
                self.state = colony.SELLECT
            else:
                self.des = mouspos
            

class ant(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        



pygame.init()
ant_tick = 0
col_tick = 0

###### list of all the sprite groups
colony_list = pygame.sprite.Group()
ant_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()

#####Screen
window = pygame.display.set_mode(SIZE)
bg_img = pygame.image.load("grass.jpg").convert()
window.blit(bg_img,(0,0,600,600))

#####Produce the map
mapload() ## this will be a funtion to load a file(.csv) and set the colong info to it
col = colony(window,(randrange(20,SIZE[0]-20),randrange(20, SIZE[1]-20)), 0)

clock = pygame.time.Clock()
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
    col.update(col_tick)   
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        loc = pygame.mouse.get_pos()
        col._mouseClick(loc)
pygame.quit()
    
    
