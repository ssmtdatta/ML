# from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import csv
import scipy
from scipy import stats


DATA_PATH = '/Users/susmitadatta/Jio/Jiobit/Data/'

usr = 'chris'
#usr = 'alex'


data = pd.read_csv(DATA_PATH+usr+'_features.csv', sep=" ")

s_thresh = 1.5  # speed threshold
t_thresh = 300  # delta_t threshold
df = data.loc[ (data['SPD'] <= s_thresh) & (data['DT'] > t_thresh) ]


coords = df.as_matrix(columns=['LAT', 'LNG'])


# g-means


n = 2 # number of clusters
kmeans_m = KMeans(n_clusters=n, init='k-means++', n_init=10, max_iter=300, tol=0.0001 ).fit(coords)
labels = kmeans_m.labels_
centroids = kmeans_m.cluster_centers_

cnt_lats = centroids[:, 0]
cnt_lngs = centroids[:, 1]

vector = [ (cnt_lats[0] - cnt_lats[1]), (cnt_lngs[0] - cnt_lngs[1]) ]

v = np.array(vector)
v2 = np.dot(v, v)   #v2 = (np.linalg.norm(v))**2

# consider cluster 1

X1 = []
X2 = []
for i in range(0, coords.shape[0]):	
  if labels[i] == 0:
    proj = np.dot(v, coords[i,:])/v2
    X1.append(proj)
  if labels[i] == 1:	
    proj = np.dot(v, coords[i,:])/v2
    X2.append(proj)

print(len(X1), len(X2))


result1 = scipy.stats.anderson(X1, dist='norm')
print(result1.statistic)

result2 = scipy.stats.anderson(X2, dist='norm')
print(result2.statistic)


  









