'''
This will be the main program where the game will run from.
'''
#lets see now
import sys
import pygame



SIZE = (400,400)
colour = pygame.color.THECOLORS

class ant(object):
    pass

class colony(object):
    
    def __init__(self,pos,size,owner=0):
        self.pos, self.size = pos, size
        self.owner = owner
        self.show(self.owner)
        
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

def exit_game():
    sys.exit()   
    
pygame.init()
screen = pygame.display.set_mode(SIZE)
screen.fill(colour["darkgreen"])
clock = pygame.time.Clock()
col = colony((100,300),10)
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





    
    
