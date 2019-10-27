import os
import random


MAX_VALUE = 1000


def generate_file(number_of_records, number_of_elements, file_name):
    data_dir = ''
    try:
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        data_dir = os.path.join(file_dir, 'data')
        os.makedirs(data_dir)
    except OSError as e:
        print('directory already exists')

    file_path = os.path.join(data_dir, file_name)

    with open(file_path, 'w') as file:
        for i in range(number_of_records):
            res = ''
            for j in range(number_of_elements):
                res += str(random.randrange(MAX_VALUE)) + ','
            res = res[:-1]
            res += '\n'
            file.write(res)


def save_to_file(data, file_name):
    data_dir = ''
    try:
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        data_dir = os.path.join(file_dir, 'data')
        os.makedirs(data_dir)
    except OSError as e:
        print('directory already exists')

    file_path = os.path.join(data_dir, file_name)

    with open(file_path, 'w') as file:
        for el in data:
            (r_val, g_val, b_val, alpha) = el
            res = str(r_val) + ',' + str(g_val) + ',' + str(b_val) + '\n'
            file.write(res)
