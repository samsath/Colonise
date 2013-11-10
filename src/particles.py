import pygame
import time
import math

SIZE=(600,600)

class ant(pygame.sprite.Sprite):
    orbit = 10
    def __init__(self,pos,vel,owner):
        '''
        The __init__ will have the position (x,y), velocity (x,y) and the owner int(1-3)
        '''
        self.pos = pos
        self.vel = vel
        self.dest = [0,0]
        self.owner = owner
        self.show(pygame.color.THECOLORS["white"])
        
    def show(self,c):
        pygame.draw.rect(window, c, self.pos,2)
        
    def setdest(self,loc):
        # this creates the destination for the ant to go to
        #use math.hypot(x,y) this will get the distance between origin and dest
        self.dest = loc
        
    def update(self):
        # this works out the distance from the dest then if closer will orbit else move towards
        if math.hypot((self.pos[0]-self.des[0]),(self.pos[1]-self.des[1])) > orbit:
            #orbit commnads
        else:
            #here to move the ant towards the destination
            

pygame.init()
window = pygame.display.set_mode(SIZE)
window.fill(pygame.color.THECOLORS["black"])

pygame.display.flip()
ant_list = pygame.sprite.Group()


while True:
    pygame.display.update()
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
pygame.quit()