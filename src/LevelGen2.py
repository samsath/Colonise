from random import randint, choice
import csv
SIZE = 11
answers = []
def find(col,colony):
    left = right = col
    
    for r,c in reversed(colony):
        left, right = left - 1, right + 1
        
        if c in (left, col, right):
            return True
    return False

def solve(n):
    if n == 0:
        return [[]]
    
    smaller_solutions = solve(n-1)
    
    return [solution+[[n,i+1]]
        for i in xrange(SIZE)
                    for solution in smaller_solutions
                        if not find(i+1, solution)]
def run():
    with open("level" + str(10) + ".csv", "wb") as f: #USE CORRECT DIRECTORY
        writer = csv.writer(f)
        personal = {1:"att",2:"def"}
        count = 0
        tobe = []
        for answer in solve(SIZE):
            answers.append(answer)
        
        choose = choice(answers)
        for i in choose:
            i[0] *= 50
            i[1] *= 50
            string = str(randint(0,3)) + "," + str(i[0]) + "," + str(i[1]) + "," + str(personal[randint(1,2)]) + "," + str(count)
            tobe.append(string)
            count += 1
        count = 0
        for i in range(randint(0,12)):
            row = choice(tobe)
            print row
            writer.writerows(row)
        
run()