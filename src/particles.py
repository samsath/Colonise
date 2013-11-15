'''
At the moment the ant is chacing the mouse when it is clicked (it goes to the location and stops)
need to add the orbit
'''

import pygame
import time
import math
from math import atan2, degrees, pi, hypot

SIZE=(600,600)


class ant(pygame.sprite.Sprite):
    orbit = 0
    def __init__(self,pos,vel,owner,picture):
        '''
        The __init__ will have the position (x,y), velocity (x,y) and the owner int(1-3)
        '''
        self.pos = pos
        self.vel = vel
        self.image = picture
        self.dest = [0,0]
        self.owner = owner
        #self.show(pygame.color.THECOLORS["white"])
        self.show(self.image)
        
    def show(self,c):
        window.blit(c,self.pos)
        
    
    def ang(self,pos1,pos2):
        '''
        pos1 = dest
        pos2 = current
        up = 90
        right = 0
        down = 270
        left = 180
        '''
        rads = atan2(-(pos2[1]-pos1[1]),(pos2[0]-pos1[0]))
        rads %= 2*pi
        degs = degrees(rads)
        return degs
        
    def setdest(self,loc):
        # this creates the destination for the ant to go to
        #use math.hypot(x,y) this will get the distance between origin and dest
        self.dest = loc
        self.update()
     
     
    def ang2(self,pos1,pos2):
        dist = [pos1[0] - pos2[0], pos1[1] - pos2[1]]
        norm = math.sqrt(dist[0] ** 2 + dist[1] ** 2 )
        return [dist[0]/norm, dist[1]/norm]
   
    def update(self):
        # this works out the distance from the dest then if closer will orbit else move towards
        if hypot((self.pos[0]-self.dest[0]),(self.pos[1]-self.dest[1])) > ant.orbit:
           # self.vel = self.ang2(self.dest,self.pos)
            posangle = self.ang(self.dest,self.pos)
            
            #old stuff
            if posangle > 0 and posangle < 90:
                self.vel = [-1,1]
            elif posangle > 90 and posangle < 180:
                self.vel = [1,1]
            elif posangle > 180 and posangle < 270:
                self.vel = [1,-1]
            elif posangle > 270 and posangle < 360:
                self.vel = [-1,-1]
            elif posangle == 0:
                self.vel = [0,1]
            elif posangle == 90:
                self.vel = [1,0]
            elif posangle == 180:
                self.vel = [0,-1]
            elif posangle == 270:
                self.vel = [-1,0] 
            
        else:
            # this will be when the particle is orbiting
            # not sure what to do here but owell
			self.vel=[0,0]
        
       # self.show(pygame.color.THECOLORS["black"])
        newpos = [int(self.pos[0]+self.vel[0]),int(self.pos[1]+self.vel[1])]
        self.pos = newpos
      #  self.show(pygame.color.THECOLORS["white"])
            

pygame.init()
window = pygame.display.set_mode(SIZE)
window.fill(pygame.color.THECOLORS["black"])
bg = pygame.image.load('grass.jpg').convert()
insect = pygame.image.load('ant.png').convert_alpha()
ants = ant((5,5),(0,0),1,insect)
pygame.display.flip()



while True:
    #pygame.time.wait(25) # this adds a 50ms delay to everything
    #window.blit(bg,(0,0))
    ants.update()
    pygame.display.update()
    event = pygame.event.poll()

    	
	
    
    
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        loc = pygame.mouse.get_pos()
        ants.setdest(loc)
pygame.quit()