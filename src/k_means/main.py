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
        gen_data.generate_file(settings.NUMBER_OF_POINTS,
            settings.NUMBER_OF_ELEMENTS, file_name)

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

    centroids, idx = run_algorithm(data, initial_centroids)

    if SET_RUN_MODE == RUN_MODE.IMAGE:
        helpers.draw_image(idx, centroids, width, height)

    print('final centroids')
    for el in centroids:
        print(el)


if __name__ == '__main__':
    main()
