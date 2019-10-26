import os
import random

plik = open("data.csv",'w+')

lines = 10000

for i in range(lines):

    plik.write(str(random.randrange(0,1000)) + ',' + str(random.randrange(0,1000))+'\n')

plik.close()
