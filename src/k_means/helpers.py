from matplotlib import pyplot
import matplotlib
from matplotlib.animation import FuncAnimation
import numpy as np
from PIL import Image
import math
import random
import gendata


def draw_image(idx, centroids, width, height):
    for el in centroids:
        print(el)

    print('width ', width)
    print('height ', height)

    data = np.zeros((height, width, 3), dtype=np.uint8)

    tempdata = centroids[idx]  #2D matrix with appropriate centroids in every row/pixel
    data = np.reshape(tempdata, data.shape) #reshape into 3D 'data' format


    '''
    l = list()
    for i in range(width):
        for j in range(height):
            sum = 0
            for k in range(3):
                data[j][i][k] = centroids[idx[i + j]][k]
                sum += data[j][i][k]
            l.append(sum)

    with open('out.txt', 'w') as file:
        res = ''
        i = 0
        for el in idx: #save idx elements line by line to out.txt
            if i == width:
                i = 0
                res += '\n'
            i += 1
            res += str(el) + ' '
        file.write(res)
    '''

    '''
    data = (data * 255).astype(np.uint8)
    img = Image.fromarray(data, 'RGB')
    img.show()
    '''

    pyplot.imshow((data).astype(np.uint8))
    pyplot.show()

def init_centroids(X, K):
    m, n = X.shape

    indexes = np.random.choice(m,K,replace = False) #generate vector with shape(K,), values from 0 to m
    centroids = X[indexes]

    #check whether centroids are not the same
    for i in range(K):                                              #for every centroid
        otherrows = centroids[np.arange(len(centroids))!=i]         #make matrix of other centroids
        if np.equal(centroids[i],otherrows).all(axis=1).any():      #if centroid is in otherrows (repeats)

            for a in range(m):                                      #for every point in data
                if not np.equal(X[a],otherrows).all(axis=1).any():  #if there is no centroid in this point
                    #print("i = " , i ," centroids before: \n", centroids)
                    centroids[i] = X[a]                             #set centroid to this point
                    #print("centroids after: \n" , centroids)
                    break

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
