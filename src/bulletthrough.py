import pygame
from pygame.sprite import Sprite
from math import sqrt

SIZE = (600,600)

class ant (Sprite):
    def __init__(self,vel):
        Sprite.__init__(self)
        self.screen = window
        self.pos = [0,0]
        self.vel = vel
        self.show(pygame.color.THECOLORS["red"])
        self.update()
        
    def show(self,c):
        pygame.draw.circle(self.screen, c, self.pos, 2)
        
    def update(self):
        newpos = [self.pos[0]+self.vel[0],self.pos[1]+self.vel[1]]
        self.pos = newpos
        self.show(pygame.color.THECOLORS["red"])
        
        

    
    
def shot(self,mouspos):
    dis = [mouspos[0] - self.pos[0],mouspos[1] - self.pos[1]]
    norm = sqrt(dis[0]**2 + dis[1]**2)
    direct = [dis[0] / norm, dis[1] / norm]
    vector = [direct[0] * sqrt(2), direct[1]*sqrt(2)]
    return vector
        
          
        
              
pygame.init()
window = pygame.display.set_mode(SIZE)
#window.fill(pygame.color.THECOLORS["black"])
ant_list = pygame.sprite.Group()
pygame.display.flip()
while True:
    for ant in ant_list:
        ant.update()
        event = pygame.event.poll()
        if event.type == pygame.Quit:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            ants = ant(window, shot(pygame.mouse.get_pos()))
            ant_list.add(ants)
            
        pygame.display.update()
pygame.quit()
