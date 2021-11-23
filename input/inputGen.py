from random import *

n = 100

seed(1)

f = open(str(n) + ".in", "w")

f.write(str(n) + "\n")

for i in range(1, n+1):
    task = str(i) + " " \
     + str(randint(1, n)) + " " \
     + str(randint(0, 1440)) + " " \
     + str(randint(0, 60)) + " " \
     + str(round(uniform(0, 100), randint(0, 5))) + "\n"
    f.write(task)

f.close()