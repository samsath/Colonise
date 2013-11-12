from math import atan2, degrees, pi, hypot
def ang(pos1,pos2):
    '''
    pos1 = dest
    pos2 = current
    up = 90
    right = 0
    down = 270
    left = 180
    '''
    rads = atan2(-(pos2[1]-pos1[1]),(pos2[0]-pos1[0]))
    rads %= 2*pi
    degs = degrees(rads)
    return degs

def update(pos,dest):
    orbit = 10
    # this works out the distance from the dest then if closer will orbit else move towards
    if hypot((pos[0]-dest[0]),(pos[1]-dest[1])) > orbit:
        posangle = ang(dest,pos)
        if posangle > 0 and posangle < 90:
            vel = [-3,3]
        elif posangle > 90 and posangle < 180:
            vel = [3,3]
        elif posangle > 180 and posangle < 270:
            vel = [3,-3]
        elif posangle > 270 and posangle < 360:
            vel = [-3,-3]
        elif posangle == 0:
            vel = [0,3]
        elif posangle == 90:
            vel = [3,0]
        elif posangle == 180:
            vel = [0,-3]
        elif posangle == 270:
            vel = [-3,0]
    else:
        vel = [0,0]
        
    newpos = [pos[0]+vel[0],pos[1]+vel[1]]
    pos[0],pos[1] = newpos[0],newpos[1]

    
pos = [5,5]
dest = [154,236]
while pos != dest:
    update(pos,dest)
    print pos