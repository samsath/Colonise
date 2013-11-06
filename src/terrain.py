'''
Put all the classes in here for the terrain
'''
import pygame

class colony(object):
    
    def __init__(self,pos,size,owner=0):
        self.pos, self.size = pos, size
        self.owner = owner
        
    def show(self):
        if self.owner == 0:
            pygame.draw.circle(screen, colour["white"], self.pos,self.size)
            
    def who_owns(self):
        return self.owner
    
    def where(self):
        return self.poS