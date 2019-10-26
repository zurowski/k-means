import os
import time

from scipy.io.matlab import loadmat
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import numpy as np

import helpers
import gendata


def run_algorithm(X, centroids, max_iters=100):
    plot_progress = False
    old_centroids = None
    if np.size(X, 1) == 2:
        plot_progress = True

    K = centroids.shape[0]
    idx = None
    idx_history = []
    centroid_history = []

    for i in range(max_iters):
        idx = helpers.find_closest_centroids(X, centroids)

        if plot_progress:
            idx_history.append(idx)
            centroid_history.append(centroids)

        centroids = helpers.generate_new_centroids(X, idx, K)

        if (centroids==old_centroids).all():
            break

        old_centroids = centroids


    if plot_progress:

        print('running animation')
        fig = pyplot.figure()
        animation = FuncAnimation(fig, helpers.plot_progress_means,
                             frames=max_iters,
                             interval=500,
                             repeat_delay=2,
                             fargs=(X, centroid_history, idx_history))
        return centroids, idx, animation

    return centroids, idx, None


def main():
    file_dir = os.path.dirname(os.path.realpath('__file__'))

    file_name = '123.csv'
    # filename = 'data_%s.txt' % time.strftime("%Y%m%d-%H%M%S")

    gendata.generate_file(1000, 2, file_name)
    file_path = os.path.join(file_dir, '../../data/' + file_name)
    data = np.transpose(np.loadtxt(file_path, skiprows=1, unpack=True, delimiter=',', dtype=int))

    X = data
    print(type(X))
    K = 4  # 3 Centroids

    initial_centroids = helpers.init_centroids(X, K)
    for el in initial_centroids:
        print(el)

    centroids, idx, animation = run_algorithm(X, initial_centroids)
    pyplot.show()


if __name__=='__main__':
    main()
