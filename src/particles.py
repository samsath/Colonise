'''
At the moment the ant is chacing the mouse when it is clicked (it goes to the location and stops)
need to add the orbit
'''

import pygame

import math
from math import degrees, atan2


SIZE=(600,600)

'''VECTOR FUNCTIONS'''
# some simple vector helper functions from http://stackoverflow.com/a/4114962/142637
def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]    

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]




class ant(pygame.sprite.Sprite):
    orbit = 0
    def __init__(self,owner,picture):
        self.x, self.y = (0,0)
        self.set_target((0, 0))
        self.speed = 0.7
        self.owner = owner
        #self.show(pygame.color.THECOLORS["white"])
        self.show(picture)
        self.angle = -90
      
    @property
    def pos(self):
        return self.x, self.y

    # for drawing, we need the position as tuple of ints
    # so lets create a helper property
    @property
    def int_pos(self):
        return map(int, self.pos)

    @property
    def target(self):
        return self.t_x, self.t_y

    @property
    def int_target(self):
        return map(int, self.target)   

    def set_target(self, pos):
        self.t_x, self.t_y = pos  
        
    def angle(self):
        return degrees(atan2(self.t_y - self.y, self.t_x - self.x))     

    def update(self):
        # if we won't move, don't calculate new vectors
        if self.int_pos == self.int_target:
            return 

        target_vector = sub(self.target, self.pos) 

        # a threshold to stop moving if the distance is to small.
        # it prevents a 'flickering' between two points
        if magnitude(target_vector) < 2: 
            return
        angle = self.angle() + 90
        # apply the ship's speed to the vector
        move_vector = [c * self.speed for c in normalize(target_vector)]

        # update position
        self.x, self.y = add(self.pos, move_vector)  
                
        
    def show(self,c):
        rot = pygame.transform.rotate(c, angle)
        rotflip = pygame.transform.flip(rot, 1, 0)
        window.blit(rotflip,self.int_pos)

pygame.init()
window = pygame.display.set_mode(SIZE)
window.fill(pygame.color.THECOLORS["black"])
bg = pygame.image.load('grass.jpg').convert()
insect = pygame.image.load('ant.png').convert_alpha()

ants = ant(1,insect)
pygame.display.flip()


while True:
    #pygame.time.wait(25) # this adds a 50ms delay to everything
    #window.blit(bg,(0,0))
    ants.update()
    window.fill(pygame.color.THECOLORS["black"])
    ants.show(insect)
    pygame.display.update()
    
    
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    if event.type == pygame.MOUSEBUTTONDOWN:
        (pygame.mouse.get_pos())
        print(pygame.mouse.get_pos())
        ants.set_target(pygame.mouse.get_pos())
    
pygame.quit()