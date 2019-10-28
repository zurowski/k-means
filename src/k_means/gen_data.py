import os
import random


MAX_VALUE = 1000


def generate_file(number_of_records, dimension, file_name):
    """
    Generate random set of data, save it to file in data directory

    :param int number_of_records: number of records in the dataset
    :param int dimension: dimension of a record (point) in dataset
    :param str file_name: name of the file in which dataset will be saved
    """
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
            for j in range(dimension):
                res += str(random.randrange(MAX_VALUE)) + ','
            res = res[:-1]
            res += '\n'
            file.write(res)


def save_to_file(data, file_name):
    """
    Save passed data to a file in data directory

    :param iterable data: data to be saved in a file
    :param str file_name: name of a file
    """
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
