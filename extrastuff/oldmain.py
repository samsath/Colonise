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

class ant(pygame.sprite.Sprite):
    
    vel=(2,2)
    
    def __init__(self,pos,dest,owner):
        self.pos = pos
        self.des = dest
        self.owner = owner
        self.show()
    
    def show(self):
        if self.owner == 0:
            pygame.draw.rect(screen, colour["black"], self.pos,2)
        if self.owner == 1:
            pygame.draw.rect(screen, colour["white"], self.pos,2)
        if self.owner == 2:
            pygame.draw.rect(screen, colour["red"], self.pos,2)
        if self.owner == 3:
            pygame.draw.rect(screen, colour["blue"], self.pos,2) 
            
            
    def nearDest(self,pos,des):
        # return boolean if the pos of the ant is within the desination
        pass
        
        
    def update(self):
        if nearDest(self.pos, self.dest):
           pass #this will orbin the dest 
        else:
            # this will head to the destination#
            pass
            
    def death(self):
        self.owenr = 0
        self.show()

class colony(pygame.sprite.Sprite):
    
    def __init__(self,pos,size,owner=1):
        self.pos, self.size = pos, size
        self.owner = owner
        self.show(self.owner)
        self.health = self.size*2
        
    def show(self,owner):
        if self.owner == 0:
            pygame.draw.circle(screen, colour["black"], self.pos,self.size)
        if self.owner == 1:
            pygame.draw.circle(screen, colour["white"], self.pos,self.size)
        if self.owner == 2:
            pygame.draw.circle(screen, colour["red"], self.pos,self.size)
        if self.owner == 3:
            pygame.draw.circle(screen, colour["blue"], self.pos,self.size)   
            
    def who_owns(self):
        return self.owner
    
    def where(self):
        return self.pos
    
    def create(self, time):
        pass
        #name = time.time()
        #name = ant(self.pos,(1,1),self.owner)
        

def exit_game():
    sys.exit()   
    
pygame.init()
screen = pygame.display.set_mode(SIZE)
screen.fill(colour["darkgreen"])
clock = pygame.time.Clock()
ant_list = pygame.sprite.Group()
col_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group() 
for ow in [1,1,1,2,3]:
    cs = randrange(10,20)
    col = colony((randrange(cs,SIZE[0]-cs),randrange(cs, SIZE[1]-cs)),cs, ow)
    col_list.add(col)

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
