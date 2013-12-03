from pygame.sprite import Sprite
from math import sqrt, hypot
import pygame

ant_image = {1:"ant.png"}
SIZE = (600,600)

class ant(Sprite):
        
    def __init__(self,screen,pos):
        Sprite.__init__(self)
        self.screen = screen
        self.pos = pos
        self.dest = pos
        
    def set_target(self,target):
        self.dest = target
        self.update()
       
       
    def show(self):
        antimg = pygame.image.load(ant_image[1]).convert_alpha()
        self.screen.blit(antimg,(self.pos[0],self.pos[1]))
            
            
    def update(self):
        #if hypot((self.pos[0] - self.dest[0]), (self.pos[1] - self.dest[1])) > 1:
        if (self.pos[0] != self.dest[0]) and (self.pos[1] != self.dest[1]):
            dist = [self.pos[0] - self.dest[0], self.pos[1] - self.dest[1]]
            norm = sqrt(dist[0] ** 2 + dist[1] ** 2)
            direct = [dist[0]/norm , dist[1]/norm]
            vel = [direct[0] * sqrt(2), direct[1] * sqrt(2)]
            print vel
        else:
            vel =[0,0]
                
            
        newpos = [(self.pos[0]+vel[0]),(self.pos[1]+vel[1])]
        self.pos = newpos
        self.show()
        

 
pygame.init() 
event = pygame.event.poll()
screen = pygame.display.set_mode(SIZE)       
screen.fill(pygame.color.THECOLORS["black"])
ants = ant(screen,(0,0))
pygame.display.flip()
while True:
    ants.update()
    pygame.display.update()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        ant.set_target(pygame.mouse.get_pos())
        print pygame.mouse.get_pos()

pygame.quit()