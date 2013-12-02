from random import randint
from math import hypot
import csv

number = 9
bases = 20
count = 100
p = 1
e1 = 8
e2 = 8
arr = [[0,0,0,0,0]]
nom = bases-p-e1-e2
i,c,z,v,b = 0,0,0,0,0

while i < bases:
    x = randint (50,550)
    y = randint (50,550)
    for j in range(len(arr)):
        if hypot((x-arr[j][1]),(y-arr[j][2])) < 100: 
            continue
    if z < nom:
        a = [0,x,y,100,i]
        arr.append(a)
        z += 1
        i += 1
        continue        
    if c < p:
        a = [1,x,y,100,i]
        arr.append(a)
        c += 1
        i += 1
        continue
    if v < e1:
        a = [2,x,y,100,i]
        arr.append(a)
        v += 1
        i += 1
        continue
    if b < e2:
        a = [3,x,y,100,i]
        arr.append(a)
        b += 1
        i += 1
        continue
arr.pop(0)
print arr
with open("/Users/Tim/Colonise/src/level" + str(number) + ".csv", "wb") as f: #USE CORRECT DIRECTORY
    writer = csv.writer(f)
    writer.writerows(arr)