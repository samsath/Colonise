'''
This will be the main program where the game will run from.
'''
#lets see now
import sys
import pygame
import time
from random import randrange



SIZE = (400,400)
colour = pygame.color.THECOLORS

class ant(object):
    def __init__(self,pos,vel,owner):
        self.pos = pos
        self.vel = vel
        self.owner = owner
        self.show()
    
    def show(self):
        if self.owner == 0:
            pygame.draw.rect(screen, colour["white"], self.pos,2)
        if self.owner == 1:
            pygame.draw.rect(screen, colour["red"], self.pos,2)
        if self.owner == 2:
            pygame.draw.rect(screen, colour["blue"], self.pos,2)
        if self.owner == 3:
            pygame.draw.rect(screen, colour["yellow"], self.pos,2) 

class colony(object):
    
    def __init__(self,pos,size,owner=0):
        self.pos, self.size = pos, size
        self.owner = owner
        self.show(self.owner)
        self.health = self.size*2
        
    def show(self,owner):
        if self.owner == 0:
            pygame.draw.circle(screen, colour["white"], self.pos,self.size)
        if self.owner == 1:
            pygame.draw.circle(screen, colour["red"], self.pos,self.size)
        if self.owner == 2:
            pygame.draw.circle(screen, colour["blue"], self.pos,self.size)
        if self.owner == 3:
            pygame.draw.circle(screen, colour["yellow"], self.pos,self.size)   
            
    def who_owns(self):
        return self.owner
    
    def where(self):
        return self.pos
    
    def create(self, time):
        name = time.time()
        name = ant(self.pos,(1,1),self.owner)
        

def exit_game():
    sys.exit()   
    
pygame.init()
screen = pygame.display.set_mode(SIZE)
screen.fill(colour["darkgreen"])
clock = pygame.time.Clock()
for ow in [0,0,0,1,2]:
    cs = randrange(10,20)
    col = colony((randrange(cs,SIZE[0]-cs),randrange(cs, SIZE[1]-cs)),cs, ow)

pygame.display.flip()


'''
Main loop
'''
while True:
    # limits the fps
    time_passed = clock.tick(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
