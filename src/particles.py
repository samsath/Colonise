import pygame
import time

SIZE=(400,400)

class ant(pygame.sprite.Sprite):
    def __init__(self,pos,vel):
        self.pos = pos
        self.vel = vel
        self.show(pygame.color.THECOLORS["white"])
        
    def show(self,c):
        pygame.draw.rect(window, c, self.pos,2)
        


pygame.init()
window = pygame.display.set_mode(SIZE)
window.fill(pygame.color.THECOLORS["black"])

pygame.display.flip()

while True:
    pygame.display.update()
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
pygame.quit()