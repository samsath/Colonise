'''
This is to try and get the splash screen and levels to work
'''

from __future__ import division
import pygame, pygame.mixer, time, math, random, csv
from pygame.locals import *
from math import hypot,atan2, degrees, pi
from random import randint, shuffle, choice

from pygame.sprite import Sprite

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

levels = {1:"level1.csv",2:"level2.csv",3:"level3.csv",
          4:"level4.csv",5:"level5.csv",6:"level6.csv",
          7:"level7.csv",8:"level8.csv",9:"level9.csv"} # list of levels as each level will be the a seperate csv file

baseimage = {0:"Colony.png",
             1:"Colony1.png",
             2:"Colony2.png",
             3:"Colony3.png"} # list of the images for the different colony objects

Logo= {"win":"WinScreen.png",
       "loss":"lossScreen.png",
       "Splash":"openScreen.png",
       "vic":"vicScreen.png"} # list of images for the different screens

colony_num = [] # this keeps track of who owns what

#SOUNDS
pygame.mixer.init(44100, -16, 2, 2048)

win = pygame.mixer.Sound('won.wav')
lost = pygame.mixer.Sound('lost.wav')
base_hit = pygame.mixer.Sound('base hit.wav')
base_alert = pygame.mixer.Sound('base alert.wav')
base_regen = pygame.mixer.Sound('base regen.wav')
base_taken = pygame.mixer.Sound('base taken.wav')
theme = pygame.mixer.Sound('theme.wav')



    
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

class game():
    '''
    This replaces the While loop at the end of the file, so that Have more control over the game process
    with this being the main process now.
    '''
    def __init__(self,level):
        #interlise all the required items for the game to run
        self.level = level
        self.clock = pygame.time.Clock()
        self.col_tick = 0
        
        ###### list of all the sprite groups
        self.colony_list = pygame.sprite.Group()
        self.ant_list = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()
        self.state = "play" # play, new, redo exit # The state is here so that we can control the player interaction as well to restart the game
        theme.play(loops = -1)
        self.answer = []
        
    def start(self):
        #this will be called after the splash screen goes away so the game will start
        self.mapload(self.level)
        self.loop()
        
    def ranstart(self):
        personal = {1:"att",2:"def"}
        count = 0
        tobe = []
        for self.answer in self.solve(11):
            self.answers.append(self.answer)
        
        choose = choice(self.answers)
        for i in choose:
            i[0] *= 50
            i[1] *= 50
            string = str(randint(0,3)) + "," + str(i[0]) + "," + str(i[1]) + "," + str(personal[randint(1,2)]) + "," + str(count)
            tobe.append(string)
            count += 1
        count = 0
        for i in range(randint(0,12)):
            row = choice(tobe)
            col = colony(self,window,(int(row[1]),int(row[2])),int(row[0]),row[3],int(row[4]))
            self.colony_list.add(col)
            colony_num.append(int(row[0])) #adds the item to the list
        self.state = "play"
        bg_img = pygame.image.load("grass.jpg").convert()
        window.blit(bg_img,(0,0,600,600))
        self.loop()
    
    def stop(self):    
        '''
        When this is called it will close the program
        '''
        pygame.quit()
    
    def find(self,col,colony):
        left = right = col
        
        for c in reversed(colony):
            left, right = left - 1, right + 1
            
            if c in (left, col, right):
                return True
        return False
    
    def solve(self,n):
        if n == 0:
            return [[]]
        
        smaller_solutions = self.solve(n-1)
        
        return [solution+[[n,i+1]]
            for i in xrange(11)
                        for solution in smaller_solutions
                            if not self.find(i+1, solution)]   
    
    
    
    def mapload(self,lev):
        '''
        This loads the level infomration from the csv and then displays it in the game
        '''
        print "load map"
        global colony_num
        colony_num = []
        #open csv file for each level
        # row 1 = x , row 2= y, row 0 = owner, row 3 = personality, row 4 numbr
        try:
            cl = csv.reader(open(levels[lev],"rU"))
        except IOError:
            # display you win the game image
            bg_vict = pygame.image.load(Logo["vic"])
            window.blit(bg_vict,(0,0,600,600))
            pygame.display.flip()        
        
        for row in cl:
            col = colony(self,window,(int(row[1]),int(row[2])),int(row[0]),row[3],int(row[4]))
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
        new_lst = filter(lambda a:a != 0, lst)
        if len(set(new_lst)) == 1:
            return new_lst[0]
        else:
            return 0
            
    def loop(self):
        '''
        This is the main game loop for the pygame
        '''
        while True:
            # Checks if there is a winner
            ch = self.check(colony_num)
            if  ch > 0:
                if ch == 1:
                    # you win
                    window.blit(pygame.image.load(Logo["win"]).convert(), (20,200,300,300))
                    self.state = "new"
                else:
                    # you loss
                    window.blit(pygame.image.load(Logo["loss"]).convert(), (20,200,300,300))
                    self.state = "redo"
                #new game  
                
            # this is all to do with the different time keeping so we can have the collony and ants move at a standard rate    
            self.clock.tick()
            elapsed = self.clock.tick(25)
            self.col_tick += elapsed




            if self.col_tick > 500:
                self.col_tick = 0         
            for a in self.ant_list:
                a.update()                          
            for c in self.colony_list: 
                c.update(self.col_tick)
                c.ai(elapsed)
                
                
            # font level indicator
            font = pygame.font.Font(None,30)
            text_level = font.render("Level: " + str(self.level), 1, colour["ht"])
            window.blit(text_level,(10,10))   
                
            pygame.display.update()
            
            # this is to allow the user input and control the game
            event = pygame.event.poll()
            
            if event.type == pygame.QUIT:
                self.stop()
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
                if self.state == "new":
                    self.level += 1
                    self.end()
                elif self.state == "redo":
                    self.end()
                elif self.state =="end":
                    self.stop()    
            
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
                self.stop()
            
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_r):
                self.end()
            if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_m):
                #mute sound here
                pass
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                if self.state == "play":
                    for c in self.colony_list:
                        c._mouseClickLeft(pygame.mouse.get_pos())
                elif self.state == "new":
                    self.level += 1
                    self.end()
                elif self.state == "redo":
                    self.end()
                elif self.state =="end":
                    self.stop()        
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
    '''
    SIZE=(20,20)
    healthmax = 10
    
    def __init__(self,game, screen, pos, owner, personality, number):
        Sprite.__init__(self)
        self.game = game
        self.screen = screen
        self.pos = pos
        self.owner = owner
        self.health = colony.healthmax # max 100
        self.inhab = 0
        self.number = number
        self.timer = 0
        self.attime = 0
        self.state = False
        self.type = personality# this is for the amount of ant the colony should have before attack
        self.show()
        self.brains = {'att':[0,0,0], 'def':[1,1,0]} #[looks after itself, attacks others, attack limit]
        self.me = self.brains[self.type] 
        self.limit = self.me[2]
        self.focus = 50
        self.burst = 10000
        self.prev = self.focus
        self.kill = (0,0)
  
    
    def healthcheck(self):
        # Checks the health level of the colony and changes the colour of the health bar accordingly
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
        if self.inhab > 99:
            tex_pos = (self.pos[0]-8,self.pos[1]-11)
        elif self.inhab > 9:
            tex_pos = (self.pos[0]-1,self.pos[1]-11)
        else:
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
                if self.owner == 1:
                    base_taken.play()
                self.state = False
                self.owner = ant.owner
                self.health = 1
                if self.owner == 1:
                    base_taken.play()
            else:
                if self.inhab > 1:                        
                    self.inhab -= 2 # element of surprise
                else:
                    if self.owner == 1:
                        base_hit.play()
                    self.health -= 1
                    if self.health < 3:
                        if self.owner == 1:
                            base_alert.play()
        else:
            if self.health < 10:
                self.health += 1
            else:
                self.inhab += 1
     

        
    def update(self ,tick):
        '''
        This updates the colony and controls it.
        Here is where the AI is for the game so play has someone to play against
        '''
        
        colony_num[self.number] = self.owner
        
        self.draw_select()
        self.show()
        
        #send the data and creates new ants
        if self.owner != 0:
            # if the colony isnt empty then it will do thing's else not
            if tick < 5:
                self.inhab += 1
                #owner 1 is user
                
######################   THE BRAINS    ###################                
                
    def ai(self, clock):

        self.timer += clock
        self.attime += clock                                                   
        
        if self.owner >= 2: #if it's an enemy

            if self.timer > self.focus:
                self.focus = randint(5000,20000)
                self.burst = randint(500,2500)
                self.timer = 0  
                print self.timer, self.focus                                              
            
            if self.me[0] != 0:             #replenish health first (apart from att)
                if self.health != 10:
                    if self.inhab > self.limit:
                        self.inhab -= 1
                        self.health += 1
                    
                r = self.game.colony_list.sprites()
                shuffle(r)    
                for c in r: #help out mates on low hp
                    if c.owner == self.owner:
                        if c.health != 10:
                            if self.attime > self.burst-150:
                                if self.inhab > self.limit:
                                    a=ants(self.game,self.pos,self.owner)
                                    a.set_target(c.pos)
                                    self.game.ant_list.add(a)
                                    self.inhab -= 1
            
            if self.focus != self.prev: 
                print 'focus', self.focus, self.prev 
                self.prev = self.focus 
                print 'prev', self.focus, self.prev             #select target
                if self.me[0] != 1:
                    r = self.game.colony_list.sprites()
                    random.shuffle(r)    
                    for c in r:
                        if c.owner != self.owner:
                            self.kill = c.pos
                            print 'TARGET CHOSEN', self.kill
                            break
                            
            if self.attime > self.burst:
                self.attime = 0
                if self.me[0] != 1:
                    if self.inhab > self.limit:
                        a=ants(self.game,self.pos,self.owner)
                        a.set_target(self.kill)
                        self.game.ant_list.add(a)
                        self.inhab -= 1
            
                                      
                                    
    def draw_select(self):
        '''
        This makes the select square on the colony only if you own it 
        '''
        sel = pygame.Surface((colony.SIZE[0]*2,colony.SIZE[1]*2))
        if self.owner == 1:
            if self.state == True:# this is to allow the user input and control the game
            
                ucolour = list(colour[self.owner])
                ucolour[3]=255
                sel.fill(ucolour)
            else:
                sel.fill((0,122,49,255))
        else:
            sel.fill((0,122,49,255))        
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
            if self.inhab > 0:
                #create ant when needed  then send it to location
                ant=ants(self.game,self.pos,self.owner)
                ant.set_target(mouspos)
                self.game.ant_list.add(ant)
                self.inhab -= 1
         
class ants(Sprite):

    def __init__(self,game,pos,owner):
        Sprite.__init__(self)
        self.game = game
        self.x, self.y = pos
        self.set_target((0, 0))
        self.speed = 3 #speeding them up for testing
        self.owner = owner
        self.angle = 0
        self.image = pygame.image.load('ant.png').convert_alpha()
        
        
    def show(self,c,image):
        if image == True:   
            rot = pygame.transform.rotate(c, self.angle) #rotate
            rotflip = pygame.transform.flip(rot, 1, 0) #flip horizontally#
            window.blit(rotflip,self.int_pos) #add to background image
        elif image == False:
            sel = pygame.Surface((12,15))
            sel.fill(colour["bg-c"])
            window.blit(sel,self.int_pos)
                
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

    def die(self):
        self.game.ant_list.remove(self)
        del self
   
    def update(self):
        self.show(self.image,False) 
        
        #This goes through the location of the ant when it stops to see if there is a collony there
        if hypot ((self.int_pos[0]-self.int_target[0]),(self.int_pos[1]-self.int_target[1])) <=5:
            for c in self.game.colony_list: # and if so runs that collonies collide code
                if hypot((c.pos[0]-self.x),(c.pos[1]-self.y)) <= 20:
                    c.collide(self) 
                else:
                    self.die()                    
                    
        target_vector = sub(self.target, self.pos) 
        # a threshold to stop moving if the distance is to small.
        # it prevents a 'flickering' between two points
        if magnitude(target_vector) < 2: 
            return

        # apply the ship's speed to the vector
        move_vector = [c * self.speed for c in normalize(target_vector)]

        # update position
        self.x, self.y = add(self.pos, move_vector)  
        #print self.x, self.y
        
        self.angle = degrees(atan2(self.t_y - self.y, self.t_x - self.x)) + 90 #calculate angle to target 


        self.show(self.image,True)            
                                    

pygame.init()
#####Screen
window = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Colonise','icon.png')
games = game(1)
bg_start = pygame.image.load("openScreen.png")
window.blit(bg_start,(0,0,600,600))
pygame.display.flip()

while True:

    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
        theme.stop()
        games.start()
    if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
        games.stop()
    if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RETURN):
        games.ranstart()
        # will be the random game mode
