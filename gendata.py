import os
import random

plik = open("dane.csv",'w+')

lines = 10000

for i in range(lines):
    x = random.randrange(0,1000)
    y = random.randrange(0,1000)

    plik.write(str(x) + ',' + str(y))

plik.close()
