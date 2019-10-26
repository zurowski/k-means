from matplotlib import pyplot
import matplotlib
from matplotlib.animation import FuncAnimation
import numpy as np
from PIL import Image
import math

import gendata


def draw_image(idx, centroids, width, height):
    for el in centroids:
        print(el)

    print('width ', width)
    print('height ', height)

    data = np.zeros((height, width, 3), dtype=np.uint8)

    l = list()
    for i in range(width):
        for j in range(height):
            sum = 0
            for k in range(3):
                data[j][i][k] = centroids[idx[i + j]][k]
                sum += data[j][i][k]
            l.append(sum)

    with open('out', 'w') as file:
        res = ''
        for el in l:
            res += str(el) + ' '
        file.write(res)

    print(type(data))

    data = (data * 255).astype(np.uint8)
    img = Image.fromarray(data, 'RGB')
    img.show()


def init_centroids(X, K):
    m, n = X.shape

    centroids = np.zeros((K, n))

    randidx = np.random.permutation(X.shape[0])
    # Take the first K examples as centroids
    centroids = X[randidx[:K], :]

    return centroids


def find_closest_centroids(X, centroids):
    K = centroids.shape[0]
    idx = np.zeros(X.shape[0], dtype=int)

    distance = np.zeros(K)
    for example in range(X.shape[0]):
        for cent in range(K):
            distance[cent] = np.sqrt(np.sum(np.power((X[example, :] - centroids[cent, :]), 2)))

        idx[example] = np.argmin(distance)
    return idx


def draw_points_animation(data, idx_history, centroid_history):
    print('running animation')
    fig = pyplot.figure()
    animation = FuncAnimation(fig, plot_progress_means,
                              frames=len(idx_history),
                              interval=500,
                              repeat_delay=2,
                              fargs=(data, centroid_history, idx_history))
    pyplot.show()


def generate_new_centroids(X, idx, K):
    # Useful variables
    m, n = X.shape
    # You need to return the following variables correctly.
    centroids = np.zeros((K, n))

    for i in range(K):
        Xtemp = X[idx == i]
        centroids[i, :] = np.sum(Xtemp, 0) / np.size(Xtemp, 0) # TODO floor

    return centroids


def plot_progress_means(i, X, centroid_history, idx_history):
    K = centroid_history[0].shape[0]
    pyplot.gcf().clf()
    cmap = pyplot.cm.rainbow
    norm = matplotlib.colors.Normalize(vmin=0, vmax=2)

    for k in range(K):
        current = np.stack([c[k, :] for c in centroid_history[:i + 1]], axis=0)
        pyplot.plot(current[:, 0], current[:, 1],
                    '-Xk',
                    mec='k',
                    lw=2,
                    ms=10,
                    mfc=cmap(norm(k)),
                    mew=2)

        pyplot.scatter(X[:, 0], X[:, 1],
                       c=idx_history[i],
                       cmap=cmap,
                       marker='o',
                       s=8 ** 2,
                       linewidths=1, )
    pyplot.grid(False)
    pyplot.title('Iteration number %d' % (i + 1))
