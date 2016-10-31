# from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import csv
import scipy
from scipy import stats

def gmeans(X, CRIT = .7):
  '''
  Recursive function to run G means algorithm.
  Arguments:
   - X: Coordinates to be potentially split up. Np.array, each row is a (lat, lng) pair
   - crit: critical value of anderson test to determine splitting
  '''

  if X.size < 10: return [X]

  # only pass in lat and lng information. Indices for later
  X_coordinates = X[:, [0, 1]]

  # Tentatively split coordinates into two clusters via k-means
  km = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, tol=0.0001 ).fit(X_coordinates)

  # calculate vector joining two cluster centers
  lat = km.cluster_centers_[:, 0]
  lng = km.cluster_centers_[:, 1]
  vector = [ (lat[0] - lat[1]), (lng[0] - lng[1]) ]

  v = np.array(vector)
  v2 = np.dot(v, v)

  # Project points from each cluster onto the vector and store in separate variables
  labels = km.labels_

  # create two clusters
  X1 = np.array([elem for index, elem in enumerate(X) if labels[index] == 0])
  X2 = np.array([elem for index, elem in enumerate(X) if labels[index] == 1])


  print "X1.size:", X1.size
  print "X2.size:", X2.size

  C1, C2 = [], []
  for i in range(0, X_coordinates.shape[0]):
    if labels[i] == 0:
      proj = np.dot(v, X_coordinates[i,:])/v2
      C1.append(proj)
    if labels[i] == 1:
      proj = np.dot(v, X_coordinates[i,:])/v2
      C2.append(proj)

  if X1.size == 0: return [X2]
  if X2.size == 0: return [X1]

  result1 = scipy.stats.anderson(C1, dist='norm')
  result2 = scipy.stats.anderson(C2, dist='norm')

  # IN CASE OF ANDERSON TEST DIVIDE BY ZERO ERROR
  # try:
  #   result1 = scipy.stats.anderson(C1, dist='norm')
  # except ZeroDivisionError:
  #   return np.concatenate((X1, gmeans(X2)))

  # try:
  #   result2 = scipy.stats.anderson(C2, dist='norm')
  # except ZeroDivisionError:
  #   return np.concatenate((gmeans(X1), X2))

  a1, a2 = result1.statistic, result2.statistic
  print a1, a2

  # both pass
  if a1 < CRIT and a2 < CRIT:
     return [X1] + [X2]

  # one fails
  if a1 > CRIT and a2 < CRIT:
    print("--A1 failed, creating new cluster--")
    return gmeans(X1) + [X2]
  if a1 < CRIT and a2 > CRIT:
    print("--A2 failed, creating new cluster--")
    return gmeans(X2) + [X1]

  # both fail
  print("--Both failed, creating new clusters--")
  return gmeans(X1) + gmeans(X2)




if __name__ == '__main__':
  # CRIT = 0.752  # significance test: critical value for alpha = 0.05

  DATA_PATH = './'
  usr = 'chris'
  #usr = 'alex'
  data = pd.read_csv(DATA_PATH+usr+'_aug_clustered.csv', sep=" ")

  indices = range(0, len(data))
  data["index"] = indices
  data_len = len(data)

  # data for clustering
  X = data.as_matrix(columns=['lat', 'lng', 'index'])

  result = gmeans(X)
  print result

  print len(result)



















