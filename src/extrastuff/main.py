'''
This is to try and get the splash screen and levels to work
'''

from __future__ import division
from math import hypot,atan2, degrees, pi
from random import randint

import pygame
from pygame.sprite import Sprite
import csv

SIZE=(600,600) # sets the size of the window

colour = {0:pygame.color.THECOLORS["white"],
          1:pygame.color.THECOLORS["red"],
          2:pygame.color.THECOLORS["blue"],
          3:pygame.color.THECOLORS["yellow"],
          "bg":pygame.color.THECOLORS["black"],
          "ht":pygame.color.THECOLORS["grey"],
          "h1":pygame.color.THECOLORS["green4"],
          "h2":pygame.color.THECOLORS["red"],
          "bg-c":(0,122,49,255),
          } # loaded colours for the different elements and bg so can all be set easily

levels = {1:"level1.csv",
          2:"level2.csv"} # list of levels as each level will be the a seperate csv file

baseimage = {0:"Colony.png",
             1:"Colony1.png",
             2:"Colony2.png",
             3:"Colony3.png"} # list of the images for the different colony objects

Logo= {"win":"WinScreen.png",
       "loss":"lossScreen.png",
       "Splash":"openScreen.png"} # list of images for the different screens

colony_num = [] # this keeps track of who owns what


def stop():    
    '''
    When this is called it will close the program
    '''
    pygame.quit()
    


class game():
    '''
    This replaces the While loop at the end of the file, so that Have more control over the game process
    with this being the main process now.
    '''
    def __init__(self,level):
        #interlise all the required items for the game to run
        self.level = level
        
        self.clock = pygame.time.Clock()
        self.ant_tick = 0
        self.col_tick = 0
        
        ###### list of all the sprite groups
        self.colony_list = pygame.sprite.Group()
        self.ant_list = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        self.state = "play" # play, new, exit # The state is here so that we can control the player interaction as well to restart the game
        
    def start(self):
        #this will be called after the splash screen goes away so the game will start
        self.mapload(self.level)
        self.loop()
    
    def mapload(self,lev):
        '''
        This loads the level infomration from the csv and then displays it in the game
        each level is a sepearate csv file. Is located in the src and referenced in the code at levels dictionary
        '''
 
        #open csv file for each level
        # row 1 = x , row 2= y, row 0 = owner, row 3 = count limit, row 4 numbr
        cl = csv.reader(open(levels[lev],"rb"))
        for row in cl:
            col = colony(self,window,(int(row[1]),int(row[2])),int(row[0]),randint(0,int(row[3])),int(row[4]))
            self.colony_list.add(col)
            colony_num.append(int(row[0])) #adds the item to the list
        self.state = "play"
        bg_img = pygame.image.load("grass.jpg").convert()
        window.blit(bg_img,(0,0,600,600))
            
    def check(self,lst):
        '''
        This checks if there is a winner or not
        As it keeps track of what colonies are ownered by what player. If all ownered by the one player then they win.
        '''
        if len(set(lst)) == 1:
            return lst[0]
        else:
            return 0
            
    def loop(self):
        '''
        This is the main game loop for the pygame
        '''
        while True:
            '''
            Uses the check function to see if all the colony owners are the same and if so that owner wins, else the game continues
            '''
            # Checks if there is a winner
            ch = self.check(colony_num)
            if  ch > 0:
                if ch == 1:
                    # you win
                    window.blit(pygame.image.load(Logo["win"]).convert(), (20,200,300,300))
                    self.level += 1
                    self.state = "new"
                else:
                    # you loss
                    window.blit(pygame.image.load(Logo["loss"]).convert(), (20,200,300,300))
                    self.state = "new"
                #new game  
                
            # this is all to do with the different time keeping so we can have the collony and ants move at a standard rate    
            self.clock.tick()
            elapsed = self.clock.tick(25)
            
            self.ant_tick += elapsed
            self.col_tick += elapsed
            if self.ant_tick > 25:
                self.ant_tick = 0
            if self.col_tick > 1000:
                self.col_tick = 0 
        
            for a in self.ant_list:
                a.update(self.ant_tick)    
                
            
            for c in self.colony_list: 
                c.update(self.col_tick)
                
            pygame.display.update()
            
            
            # this is to allow the user input and control the game
            event = pygame.event.poll()
            
            if event.type == pygame.QUIT:
                stop()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                if self.state == "play":
                    for c in self.colony_list:
                        c._mouseClickLeft(pygame.mouse.get_pos())
                elif self.state == "new":
                    self.end()
                elif self.state =="end":
                    stop()
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
               
                for c in self.colony_list:
                    c._mouseClickRight(pygame.mouse.get_pos())
                    
    def end(self):
        '''
        Once some one wins this will wipe the current game and start a new one
        '''
        for a in self.ant_list:
            self.ant_list.remove(a)
        for c in self.colony_list:
            self.colony_list.remove(c)
        self.mapload(self.level)



class colony(Sprite):
    '''
    This is the class for the collony so that we can create multiple one
    The mapload function creates each one of these. 
    '''
    SIZE=(20,20)
    healthmax = 10 # the max health of the collony
    
    def __init__(self,game, screen, pos, owner, limit, number):
        Sprite.__init__(self)
        self.game = game # makes sure it is part of the game class
        self.screen = screen # the screen is the same on all classes
        self.pos = pos # positon the x,y of the colony
        self.owner = owner # what player controls that collony
        self.health = colony.healthmax # max 10 
        self.inhab = 0 # counts how many ants there are in the colony
        self.number = number # what number it was created at  so it can be used in the game.check function to see if there are the winner
        self.state = False # This see if there user has clicked and selected the colony
        self.attack_limit = limit# this is for the amount of ant the colony should have before attack
        self.show()

  
    
    def healthcheck(self):
        '''
        Checks the health level of the colony and changes the colour of the health bar accordingly
        '''
        if self.health >= colony.healthmax/2:
            return colour["h1"]
        else:
            return colour["h2"]
    
    def show(self):
        '''
        This displays all the information of the colony onto the screen
        '''
        colimage = pygame.image.load(baseimage[self.owner]).convert_alpha()
        
        #aim is to display the health bar
        healthbg = pygame.Surface((((colony.SIZE[0]-4)*2), 10),pygame.SRCALPHA)
        healthbg.fill(colour["ht"])
        healthbar = pygame.Surface((((((colony.SIZE[0]-5)*2)/colony.healthmax)*self.health), 7),pygame.SRCALPHA)
        healthbar.fill(self.healthcheck())
        font = pygame.font.Font(None,30)
        text_suf = font.render(str(self.inhab), 1, colour["ht"])
        tex_pos = (self.pos[0]+4,self.pos[1]-11)
        
        #writes to screen
        self.screen.blit(colimage,(self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2))
        self.screen.blit(healthbg,(self.pos[0]-6,self.pos[1]+12))
        self.screen.blit(healthbar,(self.pos[0]-5,self.pos[1]+13.5))
        if self.owner == 1:
            # this is so only you can see your own army size
            self.screen.blit(text_suf,tex_pos)
            
       
            
    def collide(self,ant):
        '''
        When an ant goes into the collony it will couse the health and inhab to change depending the ant owner
        '''
        #print str(self.owner) + ", Collided with ant " + str(ant.owner)
        if ant.owner != self.owner:
            if self.health <= 1:
                self.state = False
                self.owner = ant.owner
                self.health = 1
            else:
                if self.inhab > 1:
                    self.inhab -= 3 # element of surprise
                else:
                    self.health -= 1
        else:
            if self.health < 10:
                self.health += 1
            else:
                self.inhab += 1
     

        
    def update(self ,time_passed):
        '''
        This updates the colony and controls it.
        Here is where the AI is for the game so play has someone to play against
        '''
        
        colony_num[self.number] = self.owner
        # possible add the enime AI here
        
        self.draw_select()
        self.show()
        ###################################################################################################
        ##                                        AI PART                                                ##
        ###################################################################################################
        #send the data and creates new ants
        if self.owner != 0:
            # if the colony isnt empty then it will do thing's else not
            
            if time_passed < 5:
                self.inhab += 1
                #owner 1 is user
                if self.owner >= 2:
                    for a in xrange(randint(0,self.inhab)):
                        while self.inhab >= self.attack_limit: # not enough time to build up resistance = 15
                            choose = randint(1,3)
                            if choose == 1:
                                    #attack
                                    for c in self.game.colony_list:
                                        if c.owner != self.owner:
                                            #this will send them there
    
                                                    a=ants(self.game,self.pos,(0,0),self.owner)
                                                    a.setdest(c.pos)
                                                    self.game.ant_list.add(a)
                                                    self.inhab -= 1
                            elif choose == 2:
                                #turns an ant to a health
                                if self.health != 10:
                                    self.inhab -= 1
                                    self.health += 1
                                break
                            elif choose == 3:
                                #move to other same collony
                                for c in self.game.colony_list:
                                    if c.owner == self.owner:
                                            if time_passed < 10:
                                                a=ants(self.game,self.pos,(0,0),self.owner)
                                                a.setdest(c.pos)
                                                self.game.ant_list.add(a)
                                                self.inhab -= 1
                        


    def draw_select(self):
        '''
        This makes the select square on the colony only if you own it and right click on it
        '''
        sel = pygame.Surface((colony.SIZE[0]*2,colony.SIZE[1]*2))
        if self.owner == 1:
            if self.state == True:
                ucolour = list(colour[self.owner])
                ucolour[3]=255
                sel.fill(ucolour)
            else:
                sel.fill(colour["bg-c"])
        else:
            sel.fill(colour["bg-c"])
        self.screen.blit(sel,(self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2))
        
    def _mouseClickRight(self,mouspos):    
        '''
        What happens to the collony when the button is clicked = Select the collony
        '''

        if hypot ((self.pos[0]-mouspos[0]),(self.pos[1]-mouspos[1])) <= colony.SIZE[0]*2 :
            if self.owner == 1:
                if self.state == False:
                    self.state = True
                else:
                    self.state = False
    
    def _mouseClickLeft(self,mouspos):
        '''
        What happens to the collony when the button is clicked = Send ants inhabiting the collony there
        '''

        if self.state == True:
            #if self.inhab > 0:
            if self.inhab > 0:
                #create ant when needed  then send it to location
                ant=ants(self.game,self.pos,(0,0),self.owner)
                ant.setdest(mouspos)
                self.game.ant_list.add(ant)
                self.inhab -= 1
    

     
class ants(Sprite):

    def __init__(self,game,pos,vel,owner):
        Sprite.__init__(self)
        self.game = game        # the game it is part of
        self.pos = pos          # starting pos (X,y) of the ant
        self.vel = vel          # the (x,Y) vel amount
        self.dest = [0,0]       # the ideal destination for where the ant can go
        self.owner = owner      # what player owns the ant
        self.show(colour[int(self.owner)])    # creates the ant and sets the colour of it to the owners 
        
    def show(self,c):
        '''
        Creates the ant with the owners colour
        '''
        pygame.draw.circle(window,c, self.pos,2)
        
    
    def ang(self,pos1,pos2):
        '''
        This produces the angle needed to work out its direction it needs to go
        '''
        rads = atan2(-(pos2[1]-pos1[1]),(pos2[0]-pos1[0]))
        rads %= 2*pi
        degs = degrees(rads)
        return degs
        
    def setdest(self,loc):
        '''
        This allows the collony to set the destination of the ant 
        '''
        self.dest = loc

    def die(self):
        '''
        Kills the ant and del it so that can no longer effcer the game
        '''
        self.game.ant_list.remove(self)
        del self
   
    def update(self,time_passed):
        '''
        This updates the possition of the ant by taking the vel from the pos.
        With the posangle trying to get the ant as close as possible to the destination
        '''
        if time_passed < 5:
            # this works out the distance from the dest tfor c in colony_num:
            #if hen if closer will orbit else move towards
            if hypot((self.pos[0]-self.dest[0]),(self.pos[1]-self.dest[1])) > 5:
                #self.vel = self.ang2(self.dest,self.pos)
                posangle = self.ang(self.dest,self.pos)
                
                #gets the velocity from the angle produced
                if posangle > 0 and posangle < 90:
                    self.vel = [-1,1]
                elif posangle > 90 and posangle < 180:
                    self.vel = [1,1]
                elif posangle > 180 and posangle < 270:
                    self.vel = [1,-1]
                elif posangle > 270 and posangle < 360:
                    self.vel = [-1,-1]
                elif posangle == 0:
                    self.vel = [0,1]
                elif posangle == 90:
                    self.vel = [1,0]
                elif posangle == 180:
                    self.vel = [0,-1]
                elif posangle == 270:
                    self.vel = [-1,0] 
            else:
                '''
                This goes through the location of the ant when it stops to see if there is a collony there and if so runs that collonies collide code
                '''
                for c in self.game.colony_list:

                    if hypot((c.pos[0]-self.pos[0]),(c.pos[1]-self.pos[1])) <= 20:

                        c.collide(self)
                        
                    else:
                        pass
                self.kill()
            

            self.show(colour['bg-c']) # leaFleet Foxes - White Winter Hymnalves a trail
            newpos = [int(self.pos[0]+self.vel[0]),int(self.pos[1]+self.vel[1])]
            self.pos = newpos
            self.show(colour[int(self.owner)])
                            
        

pygame.init()
'''
This bit is the splash / start screen so when the game starts you see it then you start it by clicking the space bar
'''
#####Screen
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Colonise','icon.png')

games = game(2)
bg_start = pygame.image.load("openScreen.png")
window.blit(bg_start,(0,0,600,600))
pygame.display.flip()

while True:
    # when clicked it will start the game running
    if pygame.event.poll().type==pygame.KEYDOWN:
        print "clicked"
        games.start()

