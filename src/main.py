'''
This will be the main program where the game will run from.
'''
import sys
import pygame
from terrain import colony
from ant import ant

SIZE = (400,400)
colour = pygame.color.THECOLORS

def game():
    '''
    Main game setup
    '''
    
    
    pygame.init()
    screen = pygame.display.set_mode((SIZE), 0,32)
    screen.fill(colour["darkgreen"])
    clock = pygame.time.Clock()
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


def exit_game():
    sys.exit()

if __name__ =="__main__":
    game()
    
    