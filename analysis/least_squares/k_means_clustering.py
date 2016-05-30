import numpy as np
import random


"""
K-means clustering to get clusters by tweet locations
"""


def cluster_points(X, mu):
    clusters = {}
    for x in X:
        x_coordinates = np.array((x[1], x[2]))
        best_mukey = min([(i[0], np.linalg.norm(x_coordinates - np.array((mu[i[0]][1], mu[i[0]][2]))))
                          for i in enumerate(mu)], key=lambda t: t[1])[0]
        try:
            clusters[best_mukey].append(x)
        except KeyError:
            clusters[best_mukey] = [x]
    return clusters


def reevaluate_centers(mu, clusters):
    new_mu = []
    keys = sorted(clusters.keys())
    for k in keys:
        new_mu.append(np.mean(clusters[k], axis=0))
    return new_mu


def has_converged(mu, oldmu):
    return set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu])


def find_centers(X, K):
    # Initialize to K random centers
    old_mu = random.sample(list(X), K)
    mu = random.sample(list(X), K)
    clusters = {}
    while not has_converged(mu, old_mu):
        old_mu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(old_mu, clusters)
    return mu, clusters

if __name__ == '__main__':
    import random

    X = np.array([(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(200)])

    mu, cl = find_centers(X, 20)
    print(mu, cl)






