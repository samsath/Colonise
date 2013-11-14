import pygame
from math import atan2, degrees, pi, hypot

SIZE=(600,600)


colour = {"0":pygame.color.THECOLORS["white"],
          "1":pygame.color.THECOLORS["red"],
          "2":pygame.color.THECOLORS["blue"],
          "bg":pygame.color.THECOLORS["black"],
          "ht":pygame.color.THECOLORS["grey"]
          } # change this bit to images maybe

        

class col(Sprite):
    SIZE = 20
    def __init__(self,pos,owner):
        self.pos = pos
        self.owner = owner
        self.health = 100 # max 100
        self.inhab = []
        self.show(owner)
        
    def show(self, owner):
        pygame.draw.circle(window,colour[str(owner)])
        
    def __str__(self):
        return str(self.owner) + "," + str(self.health) + "," + str(len(self.inhab))
        
    def newowner(self,owner):
        self.owner = owner
        self.show(self.owner)
        
    def healthdis(self):
        #displays the health and the inhab of the col
        pygame.draw.rect(window, colour["ht"], pygame.Rect(col.SIZE,) )
        
    def update(self,time_passed):
        # create new ants and add to list
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
            
    
        
pygame.init()
window = pygame.display.set_mode(SIZE)
window.fill(colour["bg"])
while True:
    
    pygame.display.update()
    event = pygame.event.poll()
    
    
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        loc = pygame.mouse.get_pos()
        
pygame.quit()