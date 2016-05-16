import numpy as np
import random


def cluster_points(X, mu):
    clusters = {}
    for x in X:
        best_mukey = min([(i[0], np.linalg.norm(x - mu[i[0]]))
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
    old_mu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, old_mu):
        old_mu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(old_mu, clusters)
    return mu, clusters



