# from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import csv
import scipy
from scipy import stats
import gmplot
import os
from geopy.distance import vincenty # measures distance between two locations using Vicenty's method
from random_color import random_color

# checks whether _threshold_ % of points are within _radius_ of centroid
def small_enough(X, centroid, radius = 150, threshold = 1):
  total_points = X.size
  points_outside = 0
  for point in X:
    if vincenty(centroid, (point[0], point[1])).meters >= radius:
      points_outside += 1
  if (total_points - points_outside) / float(total_points) >= threshold:
    return True
  else:
    return False



def gmeans(X, centroid = None, CRIT = 8):
  '''
  Recursive function to run G means algorithm.
  Arguments:
   - X: Coordinates to be potentially split up. Np.array, each row is a (lat, lng) pair
   - crit: critical value of anderson test to determine splitting
  '''

  if X.size < 4: return [X]
  if centroid != None and small_enough(X, centroid): return [X]

  # only pass in lat and lng information. Indices for later
  X_coordinates = X[:, [0, 1]]

  # Tentatively split coordinates into two clusters via k-means
  km = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, tol=0.0001 ).fit(X_coordinates)

  labels = km.labels_

  # create two clusters
  X1 = np.array([elem for index, elem in enumerate(X) if labels[index] == 0])
  X2 = np.array([elem for index, elem in enumerate(X) if labels[index] == 1])

  centers = km.cluster_centers_

  return gmeans(X1, centers[0]) + gmeans(X2, centers[1])



if __name__ == '__main__':
  DATA_PATH = './'
  usr = 'chris'
  data = pd.read_csv(DATA_PATH+usr+'_aug_clustered.csv', sep=" ")

  indices = range(0, len(data))
  data["index"] = indices
  data_len = len(data)

  # data for clustering
  X = data.as_matrix(columns=['lat', 'lng', 'index'])
  result = gmeans(X)
  gmap = gmplot.GoogleMapPlotter.from_geocode("Chicago", 12)

  for cluster_set in result:
    xy = []
    for elem in cluster_set:
      xy.append((elem[0], elem[1]))

    lats = [item[0] for item in xy]
    lngs = [item[1] for item in xy]
    gmap.scatter(lats, lngs, random_color(), size = 10, marker=True)

  print "NUMBER OF CLUSTERS: ", len(result)

  gmap.draw("gmeans_plot_custom_split.html")
  os.system("open gmeans_plot_custom_split.html")
