from __future__ import division
import math
from math import hypot
from random import randint

import pygame
from pygame.sprite import Sprite
import csv

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

levels = {1:"level1.csv",
          2:"level2.csv"}

baseimage = {0:"Colony.png",
             1:"Colony1.png",
             2:"Colony2.png",
             3:"Colony3.png"}


def mapload(lev):
    #open csv file for each level
    cl = csv.reader(open(levels[lev],"rb"))
    for row in cl:
        col = colony(window,(int(row[1]),int(row[2])),int(row[0]))
        colony_list.add(col)

def stop():    
    pygame.quit()
    
#########################################################
#                        Ant                            #
# some simple vector helper functions, stolen from http://stackoverflow.com/a/4114962/142637
#########################################################
def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]    

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]


class colony(Sprite):
    
    SIZE=(20,20)
    
    def __init__(self, screen, pos, owner):
        Sprite.__init__(self)
        self.screen = screen
        self.pos = pos
        self.owner = owner
        self.health = 100 # max 100
        self.inhab = pygame.sprite.Group()
        self.state = False
        self.show()
        (self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2)
   
    
    
    def healthcheck(self):
        if self.health >= 50:
            return colour["h1"]
        else:
            return colour["h2"]
      
    def show_owner(self):
        return self.owner
    
    def show_inhab(self):
        return len(self.inhab)
    
    
    def show(self):
        colimage = pygame.image.load(baseimage[self.owner]).convert_alpha()
        
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
        self.screen.blit(healthbg,(self.pos[0]-6,self.pos[1]+12))
        self.screen.blit(healthbar,((self.pos[0]-5),self.pos[1]+13.5))
        if self.owner == 1:
            # this is so only you can see your own army size
            self.screen.blit(text_suf,tex_pos)
            
       
            
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
        if self.owner != 0:
            # if the colony isnt empty then it will do thing's else not
            if time_passed % 2:
                #if self.pos != (0,0):
                if len(self.inhab) > 0:
                    for ant in self.inhab:
                        #send the ants to the mouse point
                        ant.set_target(self.pos)
                           
                
                
                ant = Ant(self.owner,insect,self.pos)
                ant_list.add(ant)
                
                self.inhab.add(ant)
                
            
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
                    for ant in ant_list:
                        if ant.owner == self.owner:
                            ant.set_target(mouspos)
                            ant.update()
                            print ant
                    self.state = False



class Ant(Sprite):
    orbit = 0
    def __init__(self,owner,picture,pos):
        Sprite.__init__(self)
        self.x, self.y = pos[0],pos[1]
        self.set_target((0, 0))
        self.speed = 0.7
        self.owner = owner
        self.pic = picture
        #self.show(pygame.color.THECOLORS["white"])
        
    
    @property
    def pos(self):
        return self.x, self.y

    # for drawing, we need the position as tuple of ints
    # so lets create a helper property
    @property
    def int_pos(self):
        return map(int, self.pos)

    @property
    def target(self):
        return self.t_x, self.t_y

    @property
    def int_target(self):
        return map(int, self.target)   

    def set_target(self, pos):
        self.t_x, self.t_y = pos

    def owner (self):
        return self.owner
        
    def update(self):
        # if we won't move, don't calculate new vectors
        if self.int_pos == self.int_target:
            return 

        target_vector = sub(self.target, self.pos) 

        # a threshold to stop moving if the distance is to small.
        # it prevents a 'flickering' between two points
        if magnitude(target_vector) < 2: 
            return

        # apply the ship's speed to the vector
        move_vector = [c * self.speed for c in normalize(target_vector)]

        # update position
        self.x, self.y = add(self.pos, move_vector) 
        self.show(self.pic)         
        
    def show(self,c):
        window.blit(c,self.int_pos)
        

class enimy():
    def __init__(self,owner):
        self.owner = owner
        self.update()
    
    def is_owned(self):
        return self.owner
        
    def update(self):
        '''
        Here needs something which goes through the list colony list if it is a
        same owner works out the inhab and if it is over a centain number it picks if it should
        send the ants to a random collony which it doens't own or build up army
        '''
        for c in colony_list:
            if c.show_owner() == self.owner:
                if c.show_inhab() > 150:
                    choose = randint(1,3)
                    if choose == 1:
                        
                        for ant in ant_list:
                            if ant.owner == self.owner:
                                ant.set_target(mouspos)
                                ant.update()
                                
                    
                    else:
                        # wait and build army
                        pass
                        
                    
                
        

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
mapload(1) ## this will be a funtion to load a file(.csv) and set the colong info to it



clock = pygame.time.Clock()

insect = pygame.image.load('ant.png').convert_alpha()


while True:

    
    pygame.display.update()
    event = pygame.event.poll()
    
    clock.tick()
    elapsed = clock.tick(100)
    
    ant_tick += elapsed
    col_tick += elapsed
    if ant_tick > 25:
        ant_tick = 0
    if col_tick > 1000:
        col_tick = 0 
    
    for a in ant_list:
        a.update()    
        
    
    for c in colony_list: 
        c.update(col_tick)
    
    #pygame.sprite.groupcollide(ant_list, colony_list, True, False)
           
    if event.type == pygame.QUIT:
        stop()
    if event.type == pygame.MOUSEBUTTONDOWN:
        loc = pygame.mouse.get_pos()
        for c in colony_list:
            c._mouseClick(loc)
 