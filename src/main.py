'''
This will be the main program where the game will run from.
'''
import sys
import pygame

def game():
    '''
    Main game setup
    '''
    SCREEN_WIDTH,SCREEN_HEIGHT = 400,400
    
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0,32)
    
    clock = pygame.time.Clock()
    
    
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
    
    