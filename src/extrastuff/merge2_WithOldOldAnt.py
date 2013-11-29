'''
This is to try and get the rest of the program to work
while ant doesn't
'''


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
       "Splash":"openScreen.png"}

colony_num = [] # this keeps track of who owns what

def mapload(lev):
    #open csv file for each level
    # row 1 = x , row 2= y, row 0 = owner, row 3 = count limit, row 4 numbr
    cl = csv.reader(open(levels[lev],"rb"))
    for row in cl:
        col = colony(window,(int(row[1]),int(row[2])),int(row[0]),randint(0,int(row[3])),int(row[4]))
        colony_list.add(col)
        colony_num.append(int(row[0])) #adds the item to the list

def stop():    
    pygame.quit()
    
def check(lst):
    if len(set(lst)) == 1:
        return lst[0]
    else:
        return 0

class colony(Sprite):
    
    SIZE=(20,20)
    
    def __init__(self, screen, pos, owner, limit, number):
        Sprite.__init__(self)
        self.screen = screen
        self.pos = pos
        self.owner = owner
        self.health = 10 # max 100
        self.inhab = 0
        self.number = number
        self.state = False
        self.attack_limit = limit# this is for the amount of ant the colony should have before attack
        self.show()
        (self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2)
  
    
    def healthcheck(self):
        if self.health >= 5:
            return colour["h1"]
        else:
            return colour["h2"]
    
    def show(self):
        colimage = pygame.image.load(baseimage[self.owner]).convert_alpha()
        
        #aim is to display the health bar
        healthbg = pygame.Surface((((colony.SIZE[0]-4)*2), 10),pygame.SRCALPHA)
        healthbg.fill(colour["ht"])
        healthbar = pygame.Surface((((((colony.SIZE[0]-5)*2)/10)*self.health), 7),pygame.SRCALPHA)
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
        #print str(self.owner) + ", Collided with ant " + str(ant.owner)
        if ant.owner != self.owner:
            if self.health <= 1:
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
        colony_num[self.number] = self.owner
        # possible add the enime AI here
        
        self.draw_select()
        self.show()
        
        #send the data and creates new ants
        if self.owner != 0:
            # if the colony isnt empty then it will do thing's else not
            if time_passed < 5:
                self.inhab += 1
            #owner 1 is user
            if self.owner >= 2:
                while self.inhab >= self.attack_limit: # not enough time to build up resistance = 15
                    choose = randint(1,3)
                    if choose == 1:
                            #attack
                            for c in colony_list:
                                if c.owner != self.owner:
                                    #this will send them there
                                    ant=ants(self.pos,(0,0),self.owner)
                                    ant.setdest(c.pos)
                                    ant_list.add(ant)
                                    self.inhab -= 1
                    elif choose == 2:
                        # this will hopefully build up the army
                        break
                    elif choose == 3:
                        #move to other same collony
                        for c in colony_list:
                            if c.owner == self.owner:
                                #this will send them there
                                ant=ants(self.pos,(0,0),self.owner)
                                ant.setdest(c.pos)
                                ant_list.add(ant)
                                self.inhab -= 1
                


    def draw_select(self):
        if self.owner == 1:
            sel = pygame.Surface((colony.SIZE[0]*2,colony.SIZE[1]*2))
            if self.state == True:
                ucolour = list(colour[self.owner])
                ucolour[3]=255
                sel.fill(ucolour)
            else:
                sel.fill((0,122,49,255))
                
            self.screen.blit(sel,(self.pos[0]-colony.SIZE[0]/2,self.pos[1]-colony.SIZE[1]/2))
        
    def _mouseClickRight(self,mouspos):    

        if hypot ((self.pos[0]-mouspos[0]),(self.pos[1]-mouspos[1])) <= colony.SIZE[0]*2 :
            if self.owner == 1:
                if self.state == False:
                    self.state = True
                else:
                    self.state = False
    
    def _mouseClickLeft(self,mouspos):

            if self.state == True:
                #if self.inhab > 0:
                if self.inhab > 0:
                    #create ant when needed  then send it to location
                    ant=ants(self.pos,(0,0),self.owner)
                    ant.setdest(mouspos)
                    ant_list.add(ant)
                    self.inhab -= 1
    

     
class ants(Sprite):

    def __init__(self,pos,vel,owner):
        Sprite.__init__(self)
        self.pos = pos
        self.vel = vel
        self.dest = [0,0]
        self.owner = owner
        self.show(colour[0])
        
    def show(self,c):
        pygame.draw.circle(window,c, self.pos,2)
        
    
    def ang(self,pos1,pos2):

        rads = atan2(-(pos2[1]-pos1[1]),(pos2[0]-pos1[0]))
        rads %= 2*pi
        degs = degrees(rads)
        return degs
        
    def setdest(self,loc):
        # this creates the destination for the ant to go to
        #use math.hypot(x,y) this will get the distance between origin and dest
        self.dest = loc

    def die(self):
        ant_list.remove(self)
        del self
   
    def update(self,time_passed):
        if time_passed < 5:
            # this works out the distance from the dest tfor c in colony_num:
            #if hen if closer will orbit else move towards
            if hypot((self.pos[0]-self.dest[0]),(self.pos[1]-self.dest[1])) > 5:
                #self.vel = self.ang2(self.dest,self.pos)
                posangle = self.ang(self.dest,self.pos)
                
                #old stuff
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
                
                for c in colony_list:

                    if hypot((c.pos[0]-self.pos[0]),(c.pos[1]-self.pos[1])) <= 20:

                        c.collide(self)
                        
                    else:
                        pass
                self.kill()
            

            self.show(colour['bg-c']) # leaFleet Foxes - White Winter Hymnalves a trail
            newpos = [int(self.pos[0]+self.vel[0]),int(self.pos[1]+self.vel[1])]
            self.pos = newpos
            self.show(colour[0])
                            
        

pygame.init()
ant_tick = 0
col_tick = 0

###### list of all the sprite groups
colony_list = pygame.sprite.Group()
ant_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()

#####Screen
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Colonise','icon.png')
icon = pygame.image.load('icon.png').convert()
pygame.display.set_icon(icon)
bg_img = pygame.image.load("grass.jpg").convert()
window.blit(bg_img,(0,0,600,600))

#####Produce the map
mapload(1) ## this will be a funtion to load a file(.csv) and set the colong info to it



clock = pygame.time.Clock()

insect = pygame.image.load('ant.png').convert_alpha()




while True:
    ch = check(colony_num)
    if  ch > 0:
        if ch == 1:
            # you win
            window.blit(pygame.image.load(Logo["win"]).convert(), (20,200,300,300))
        else:
            # you loss
            window.blit(pygame.image.load(Logo["loss"]).convert(), (20,200,300,300))
        #new game
        
    
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
