from __future__ import division
from math import hypot,atan2, degrees, pi
from random import randint

import pygame
from pygame.sprite import Sprite
import csv

SIZE=(600,600)

colour = {0:pygame.color.THECOLORS["white"],
          1:pygame.color.THECOLORS["red"],
          2:pygame.color.THECOLORS["blue"],
          3:pygame.color.THECOLORS["yellow"],
          "bg":pygame.color.THECOLORS["black"],
          "ht":pygame.color.THECOLORS["grey"],
          "h1":pygame.color.THECOLORS["green4"],
          "h2":pygame.color.THECOLORS["red"],
          "bg-c":(0,122,49,255),
          } # change this bit to images maybe

levels = {1:"level1.csv",
          2:"level2.csv"}

baseimage = {0:"Colony.png",
             1:"Colony1.png",
             2:"Colony2.png",
             3:"Colony3.png"}

Logo= {"win":"WinScreen.png",
       "loss":"lossScreen.png",
       "Splash":"openScreen.png",
       "grass":"grass.jpg"}

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode(SIZE)
        pygame.display.set_caption('Colonise','icon.png')
        self.game = Game()
        # background here
        bg_img = pygame.image.load(Logo("Splash")).convert()
        self.blit(bg_img,(0,0,600,600))
        
        ###### list of all the sprite groups
        colony_list = pygame.sprite.Group()
        ant_list = pygame.sprite.Group()
        all_sprite_list = pygame.sprite.Group()
        
        self.loop()
    
    def loop(self):
        pygame.display.update()
        event = pygame.event.poll()
        
        clock.tick()
        elapsed = clock.tick(25)
        
        ant_tick += elapsed
        col_tick += elapsed
        
        if ant_tick > 25:
            ant_tick = 0
        if col_tick > 1000:
            col_tick = 0
        
        for a in ant_list:
            a.update(ant_tick)    
        
    
        for c in colony_list: 
            c.update(col_tick)
            
        if event.type == pygame.QUIT:
            stop()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for c in colony_list:
                c._mouseClickLeft(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            for c in colony_list:
                c._mouseClickRight(pygame.mouse.get_pos())
            