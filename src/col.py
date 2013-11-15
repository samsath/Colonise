from __future__ import division
import pygame
from random import randrange

#from math import atan2, degrees, pi, hypot

SIZE=(600,600)


colour = {"0":pygame.color.THECOLORS["white"],
          "1":pygame.color.THECOLORS["red"],
          "2":pygame.color.THECOLORS["blue"],
          "bg":pygame.color.THECOLORS["black"],
          "ht":pygame.color.THECOLORS["grey"],
          "h1":pygame.color.THECOLORS["green"],
          "h2":pygame.color.THECOLORS["red"]
          } # change this bit to images maybe

        

class collony():
    SIZE = 20
    def __init__(self,pos,owner):
        self.pos = pos
        self.owner = owner
        self.health = 100 # max 100
        self.inhab = []
        self.show(self.owner)
        
    def show(self, owner):
        # displays the colony on the map
        pygame.draw.circle(window,colour[str(owner)],self.pos,collony.SIZE) 
        self.healthdis()
        
        
    def __str__(self):
        # returns the information about the col to the computer
        return str(self.owner) + "," + str(self.health) + "," + str(len(self.inhab))

    def healthcheck(self):
        if self.health >= 50:
            return colour["h1"]
        else:
            return colour["h2"]
        
    def healthdis(self):
        #displays the health and the inhab of the col
        num = len(self.inhab)
        pygame.draw.rect(window, colour["ht"], pygame.Rect(self.pos[0]-collony.SIZE,self.pos[1]+5, (collony.SIZE-4)*2, 10))
        pygame.draw.rect(window, self.healthcheck(), pygame.Rect(self.pos[0]-collony.SIZE,self.pos[1]+5, int(((collony.SIZE*2)/100)*self.health), 9)) 
        font = pygame.font.Font(None,30)
        text_suf = font.render(str(num), 1, colour["ht"])
        tex_pos = (self.pos[0]-collony.SIZE/4,self.pos[1]-collony.SIZE)
        window.blit(text_suf,tex_pos)
        
        
    def update(self,time_passed):
        # create new ants and add to list
        if self.owner != 0:
            #make ant
            pass
        
        
    def mouse_click_event(self,pos):
        '''
        Will be here when you click on it and then click somewhere else it will send the ants
        '''
        pass
        
    def attacked(self,value):
        #decrease health after destroying the inhab
        if len(self.inhab) > 0:
            del self.inhab[0]
        else:
            self.health -= value
        
        self.healthdis()
        if self.health == 0:
            self.owner = 0
            self.health = 100
            
    def inhabit(self, ant):
        if self.owner == ant.owner:
            if self.health < 100:
                self.health += 1
            else:
                self.inhab.append(ant) # this will be the ant I think
        else:
            if self.health == 0:
                self.owner = ant.owner
    
  
class ant(object):
    def __init__(self,visible,owner,pos,vel):
        self.vis = visible
        self.owner = owner
        self.pos = pos
        self.vel = vel
        
    def show(self):
        if self.vis == True:
            pygame.draw.circle(window,colour[str(self.owner)],self.pos,1) 
        else:
            trans = list(colour[str(self.owner)])
            trans[3]=0
            pygame.draw.circle(window,trans,self.pos,collony.SIZE) 
        
    def update(self):
        newpos = [self.pos[0]+self.vel[0],self.pos[1]+self.vel[1]]
        self.pos = newpos

pygame.init()
window = pygame.display.set_mode(SIZE)
window.fill(colour["bg"])
col = collony((randrange(20,SIZE[0]-20),randrange(20, SIZE[1]-20)), 0)
while True:
    
    pygame.display.update()
    event = pygame.event.poll()
    
    
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        loc = pygame.mouse.get_pos()
        
pygame.quit()