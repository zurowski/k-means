import os
import time

from scipy.io.matlab import loadmat
from matplotlib import pyplot

import numpy as np

import helpers
import gendata
import image_loader


def run_algorithm(X, centroids, max_iters=10):
    # for drawing 2d animation after algorithm is
    plot_progress = False

    old_centroids = None

    if np.size(X, 1) == 2:
        plot_progress = True

    K = centroids.shape[0]
    idx = None
    idx_history = []
    centroid_history = []

    for i in range(max_iters):
        print('tick')
        idx = helpers.find_closest_centroids(X, centroids)

        if plot_progress:
            idx_history.append(idx)
            centroid_history.append(centroids)

        centroids = helpers.generate_new_centroids(X, idx, K)

        if (centroids == old_centroids).all():
            break

        old_centroids = centroids

    # TODO
    if plot_progress:
        helpers.draw_points_animation(X, idx_history, centroid_history)

    return centroids, idx


def main():
    file_dir = os.path.dirname(os.path.realpath('__file__'))

    file_name = 'image_pixels.png'

    # filename = 'data_%s.txt' % time.strftime("%Y%m%d-%H%M%S")
    # gendata.generate_file(1000, 2, file_name)

    width, height = image_loader.load_image('image2.png', 'image_pixels.png')

    file_path = os.path.join(file_dir, '../../data/' + file_name)
    data = np.transpose(np.loadtxt(file_path, skiprows=1, unpack=True, delimiter=',', dtype=int))

    X = data
    print(type(X))
    K = 4  # 3 Centroids

    initial_centroids = helpers.init_centroids(X, K)
    for el in initial_centroids:
        print(el)

    centroids, idx = run_algorithm(X, initial_centroids)
    helpers.draw_image(idx, centroids, width, height)


if __name__ == '__main__':
    main()
