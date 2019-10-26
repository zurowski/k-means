import os
import random

NUMBER_OF_RECORDS = 10000
NUMBER_OF_ELEMENTS = 3

MAX_VALUE = 1000

random_name = 'data_%s.txt' % random.randrange(100000)
file_dir = os.path.dirname(os.path.realpath('__file__'))
file_path = os.path.join(file_dir, '../../data/' + random_name)

with open(file_path, 'w') as file:
    for i in range(NUMBER_OF_RECORDS):
        res = ''
        for i in range(NUMBER_OF_ELEMENTS):
            res += str(random.randrange(MAX_VALUE)) + ','
        res = res[:-1]
        res += '\n'
        file.write(res)

