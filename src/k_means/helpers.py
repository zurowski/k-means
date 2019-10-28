import random
import numpy as np
import matplotlib
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation


def draw_image(idx, centroids, width, height):
    """
    Draw new, compressed image

    :param idx: vector of record numbers of centroids assigned to every pixel
     in the image
    :param centroids: matrix of centroids, where every centroid defines
     one colour in RGB scale
    :param width: width of the picture
    :param height: height of the picture
    """

    data = np.zeros((height, width, 3), dtype=np.uint8)

    temp_data = centroids[idx]
    data = np.reshape(temp_data, data.shape)

    pyplot.imshow(data.astype(np.uint8))
    pyplot.show()


def init_centroids(data, k):
    """
    Create initial matrix of centroids, where every row is unique
    (every centroid is initialized in a different location)

    :param data: data which select centroids from
    :param k: number of centroids
    :return: matrix of newly created centroids
    """
    
    m, n = data.shape

    indexes = np.random.choice(m, k, replace=False)
    centroids = data[indexes]

    for i in range(k):
        other_rows = centroids[np.arange(len(centroids)) != i]
        if np.equal(centroids[i], other_rows).all(axis=1).any():
            for a in range(m):
                index = random.randrange(m)
                if not np.equal(data[index], other_rows).all(axis=1).any():
                    centroids[i] = data[index]
                    break

    return centroids


def find_closest_centroids(data, centroids):
    """
    Group points of data in clusters by computing distance between points
    and every single centroid and choosing the closest centroid

    :param data: points of data where every row is one point
    :param centroids: matrix of locations of centroids in multidimensional
     space, where every row is one centroid
    :return: vector of record numbers of centroids assigned to every
     point in data
    """

    k = centroids.shape[0]
    idx = np.zeros(data.shape[0], dtype=int)
    distance = np.zeros(k)
    for example in range(data.shape[0]):
        for cent in range(k):
            distance[cent] = np.sqrt(np.sum(np.power((data[example, :] -
                                                      centroids[cent, :]), 2)))

        idx[example] = np.argmin(distance)
    return idx


def generate_new_centroids(data, idx, k):
    """
    Compute new location of every centroid by calculating mean from every point
    assigned to that specific centroid

    :param data: points of data where every row is one point
    :param idx: vector of record numbers of centroids assigned to every point in data
    :param k: number of centroids
    :return: matrix of locations of new centroids
    """

    m, n = data.shape
    centroids = np.zeros((k, n))

    for i in range(k):
        x_temp = data[idx == i]
        centroids[i, :] = np.sum(x_temp, 0) / np.size(x_temp, 0)

    return centroids


def draw_points_animation(data, idx_history, centroid_history):
    """

    :param data:
    :param idx_history:
    :param centroid_history:
    :return:
    """
    print('running animation')
    fig = pyplot.figure()
    animation = FuncAnimation(fig, plot_progress_means,
                              frames=len(idx_history),
                              interval=500,
                              repeat_delay=2,
                              fargs=(data, centroid_history, idx_history))
    pyplot.show()


def plot_progress_means(i, data, centroid_history, idx_history):
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

        pyplot.scatter(data[:, 0], data[:, 1],
                       c=idx_history[i],
                       cmap=cmap,
                       marker='o',
                       s=8 ** 2,
                       linewidths=1, )
    pyplot.grid(False)
    pyplot.title('Iteration number %d' % (i + 1))
