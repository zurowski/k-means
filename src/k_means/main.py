import sys
import os
import time
import numpy as np
from enum import Enum

import helpers
import settings
import image_loader
import gen_data


class RUN_MODE(Enum):
    POINTS = 1
    IMAGE = 2


SET_RUN_MODE = 0


def run(data, centroids, max_iters=20):
    """
    Run algorithm, in POINTS mode save metadata to history

    :param np.array data: points of data where every row is one point
    :param np.array centroids: matrix of locations of centroids in multidimensional
     space, where every row is one centroid
    :param int max_iters: number of iterations after which algorithm would stop if it
     had not converged earlier
    :return np.array, np.array: final centroids and idx
    """
    old_centroids = None

    k = centroids.shape[0]

    # idx keeps corresponding centroid for every entry in data
    idx = None

    idx_history = []
    centroid_history = []

    for i in range(max_iters):
        print('tick')
        idx = helpers.find_closest_centroids(data, centroids)

        if SET_RUN_MODE == RUN_MODE.POINTS and settings.DIMENSION == 2:
            idx_history.append(idx)
            centroid_history.append(centroids)

        centroids = helpers.generate_new_centroids(data, idx, k)

        if (centroids == old_centroids).all():
            # if no changes in centroids happened, end algorithm
            break

        old_centroids = centroids

    if SET_RUN_MODE == RUN_MODE.POINTS and settings.DIMENSION == 2:
        helpers.draw_points_animation(data, idx_history, centroid_history)

    return centroids, idx


def main():
    global SET_RUN_MODE

    if len(sys.argv) != 2:
        print('Usage: <mode>')
        sys.exit(-1)
    else:
        if sys.argv[1] == 'IMAGE':
            SET_RUN_MODE = RUN_MODE.IMAGE
        elif sys.argv[1] == 'POINTS':
            SET_RUN_MODE = RUN_MODE.POINTS
        else:
            print('Available modes:')
            for el in RUN_MODE:
                print(str(el).split('.')[1])
            sys.exit(-1)

    file_dir = os.path.dirname(os.path.realpath('__file__'))

    file_name = ''
    if settings.SOURCE_FILE is not None:
        file_name = settings.SOURCE_FILE
    else:
        file_name = 'data_%s.txt' % time.strftime("%Y%m%d-%H%M%S")

    if SET_RUN_MODE == RUN_MODE.POINTS:
        gen_data.generate_file(settings.NUMBER_OF_POINTS,
                               settings.DIMENSION, file_name)

    data_dir_path = os.path.join(file_dir, 'data')
    print(data_dir_path)

    width, height = 0, 0
    if SET_RUN_MODE == RUN_MODE.IMAGE:
        source_image_name = settings.SOURCE_IMAGE_NAME
        width, height = image_loader.load_image(
            os.path.join(data_dir_path, source_image_name), file_name)

    data = np.transpose(np.loadtxt(os.path.join(data_dir_path, file_name),
                                   unpack=True, delimiter=',', dtype=int))

    k = settings.K

    initial_centroids = helpers.init_centroids(data, k)

    print('Initialized centroids')
    for el in initial_centroids:
        print(el)

    centroids, idx = run(data, initial_centroids)

    print('Final centroids')
    for el in centroids:
        print(el)

    if SET_RUN_MODE == RUN_MODE.IMAGE:
        helpers.draw_image(idx, centroids, width, height)


if __name__ == '__main__':
    main()
