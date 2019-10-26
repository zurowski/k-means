import os

from scipy.io.matlab import loadmat
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

import helpers


def run_algorithm(X, centroids, max_iters=10, plot_progress=True):
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

    if plot_progress:
        print('running animation')
        fig = pyplot.figure()
        animation = FuncAnimation(fig, helpers.plot_progress_means,
                             frames=max_iters,
                             interval=500,
                             repeat_delay=2,
                             fargs=(X, centroid_history, idx_history))
        return centroids, idx, animation

    return centroids, idx


def main():
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(file_dir, '../../data/ex7data2.mat')
    data = loadmat(filename)
    X = data['X']
    print(type(X))
    K = 3  # 3 Centroids

    initial_centroids = helpers.init_centroids(X, K)
    for el in initial_centroids:
        print(el)

    centroids, idx, animation = run_algorithm(X, initial_centroids, 10)
    pyplot.show()


if __name__=='__main__':
    main()