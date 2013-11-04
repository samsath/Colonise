'''
Put all the classes in here for the terrain
'''

class colony(object):
    
    def __init__(self,pos,size,owner=0):
        self.pos, self.size = pos, size
        self.owner = owner
        
    def show(self,owner):
        