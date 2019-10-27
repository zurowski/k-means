import sys
import os
import numpy as np
import time
import helpers
import settings
import image_loader
import gendata

from enum import Enum


class RUN_MODE(Enum):
    POINTS = 1
    IMAGE = 2


SET_RUN_MODE = 0


def run_algorithm(data, centroids, max_iters=10):

    old_centroids = None

    k = centroids.shape[0]
    idx = None
    idx_history = []
    centroid_history = []

    for i in range(max_iters):
        print('tick')
        idx = helpers.find_closest_centroids(data, centroids)

        if SET_RUN_MODE == RUN_MODE.POINTS:
            idx_history.append(idx)
            centroid_history.append(centroids)

        centroids = helpers.generate_new_centroids(data, idx, k)

        if (centroids == old_centroids).all():
            break

        old_centroids = centroids

    if SET_RUN_MODE == RUN_MODE.POINTS:
        helpers.draw_points_animation(data, idx_history, centroid_history)

    return centroids, idx


def main():

    global SET_RUN_MODE
    if len(sys.argv) != 2:
        print('Usage <mode>')
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

    file_dir = os.path.dirname(os.path.realpath('__file__'))

    file_name = ''
    if settings.SOURCE_FILE is not None:
        file_name = settings.SOURCE_FILE
    else:
        file_name = 'data_%s.txt' % time.strftime("%Y%m%d-%H%M%S")

    if SET_RUN_MODE == RUN_MODE.POINTS:
        gendata.generate_file(1000, 2, file_name)

    data_dir_path = os.path.join(file_dir, 'data/')
    print(data_dir_path)

    width, height = 0, 0
    if SET_RUN_MODE == RUN_MODE.IMAGE:
        width, height = image_loader.load_image(os.path.join(data_dir_path, file_name), 'image_pixels.txt')

    #data = np.transpose(np.loadtxt(data_dir_path,  unpack=True, delimiter=',', dtype=int))

    # k = settings.K
    #
    # initial_centroids = helpers.init_centroids(data, k)
    #
    # print('Initialized centroids')
    # for el in initial_centroids:
    #     print(el)
    #
    # centroids, idx = run_algorithm(data, initial_centroids)
    #
    # if SET_RUN_MODE == RUN_MODE.IMAGE:
    #     helpers.draw_image(idx, centroids, width, height)


if __name__ == '__main__':
    main()
