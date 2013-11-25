import pygame
from pygame.sprite import Sprite
from math import hypot,sqrt

SIZE = (600,600)

class ant (Sprite):
    def __init__(self,vel):
        Sprite.__init__(self)
        self.screen = window
        self.pos = (20,20)
        self.vel = pos
        self.show(pygame.color.THECOLORS["red"])
        
    def show(self,c):
        pygame.draw.circle(self.screen, c, self.pos, 2)
        
    def update(self):
        newpos = [self.pos[0]+self.vel[0],self.pos[1]+self.vel[1]]
        self.pos = newpos
        self.show(pygame.color.THECOLORS["red"])
        
        
class gun():
    def _init__(self,screen):
        self.screen = screen
        self.pos = (20,20)
        self.sellect = False
        
    def show(self):
        pygame.draw.circle(self.screen, pygame.color.THECOLORS["white"], self.pos, 20)
    
    def shot(self,mouspos):
        dis = [mouspos[0] - self.pos[0],mouspos[1] - self.pos[1]]
        norm = sqrt(dis[0]**2 + dis[1]**2)
        direct = [dis[0] / norm, dis[1] / norm]
        vector = [direct[0] * sqrt(2), direct[1]*sqrt(2)]
        return vector
        
        
        
    def _mouseClick(self,mouspos):
        if hypot ((self.pos[0]-mouspos[0]),(self.pos[1]-mouspos[1])) <= 20 :
            if self.sellect == False:
                self.sellect = True
                print "selected"
            else:
                self.sellect = False
        else:
            if self.sellect == True:
                ants = ant(self.screen, self.shot(mouspos))
                ant_list.add(ants)
            
        
              
pygame.init()
window = pygame.display.set_mode(SIZE)
window.fill(pygame.color.THECOLORS["black"])
ant_list = pygame.sprite.Group()
guns = gun()
pygame.display.flip()
while True:
    for ant in ant_list:
        ant.update()
        event = pygame.event.poll()
        if event.type == pygame.Quit:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            gun._mouseClick(pygame.mouse.get_pos())
        pygame.display.update()
pygame.quit()
