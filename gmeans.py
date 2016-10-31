# from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import csv
import scipy
from scipy import stats


global CRIT
CRIT = 0.752  # significance test: critical value for alpha = 0.05
SPLIT = True




def kmeansCluster(X, k):
  kmeans_m = KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, tol=0.00001 ).fit(X)
  return kmeans_m.labels_, kmeans_m.cluster_centers_


def projection(x, y):
  vector = [ (x[0] - x[1]), (y[0] - y[1]) ]
  v = np.array(vector)
  v2 = np.dot(v, v) 
  C1 = []
  C2 = []
  for i in range(0, coords.shape[0]):	
    if labels[i] == 0:
      proj = np.dot(v, coords[i,:])/v2
      C1.append(proj)
    if labels[i] == 1:	
      proj = np.dot(v, coords[i,:])/v2
      C2.append(proj) 
  return C1, C2      


def normalityTest(C1, C2):
  result1 = scipy.stats.anderson(C1, dist='norm')
  result2 = scipy.stats.anderson(C2, dist='norm')
  return result1.statistic, result2.statistic

def prepare_data():
  pass  

def gmeans():
    


# g-means
#------------------------------------------------
DATA_PATH = '/Users/susmitadatta/Jio/Jiobit/Data/'
usr = 'chris'
#usr = 'alex'
data = pd.read_csv(DATA_PATH+usr+'_features.csv', sep=" ")
s_thresh = 1.5  # speed threshold
t_thresh = 600  # delta_t threshold
df = data.loc[ (data['SPD'] <= s_thresh) & (data['DT'] > t_thresh) ]




# this part needs to go in a function
coords = df.as_matrix(columns=['LAT', 'LNG']) 
# initial clustering 
labels, centroids = kmeansCluster(coords, k=2)
cnt_lats = centroids[:, 0]  
cnt_lngs = centroids[:, 1]

C1, C2 = projection(cnt_lats, cnt_lngs) ## need to generalize for n-dimension
a1, a2 = normalityTest(C1, C2)
 
idx1 = np.where(labels==0)[0]
idx2 = np.where(labels==1)[0]



while split_1:
  if a1 <= CRIT:
    # separate label 0
    df1_labeled = df.ix[idx1] # <== add labels to dataframe
    split_1 = False
  else:
    df1 = df.ix[idx1]	# <== cannot modify original df
    split_1 = True

    coords = df1.as_matrix(columns=['LAT', 'LNG']) 
    labels, centroids = kmeansCluster(coords)
    cnt_lats = centroids[:, 0]  
    cnt_lngs = centroids[:, 1]
    C1, C2 = projection(cnt_lats, cnt_lngs) ## need to generalize for n-dimension
    a1, a2 = normalityTest(C1, C2)
 
    idx1 = np.where(labels==0)[0]
    idx2 = np.where(labels==1)[0]





# while split_2:
#   if a2 <= CRIT:
#     # separate label 1
#     df2_labeled = df.ix[idx2]
#     #==> add labels to dataframe
#     split_2 = False
#   else:
#     df2 = df.ix[idx2]	
#     split_2 = True	

# #frames = [df1, df2, df3]

# if (split_1 == False) and (split_2 == False):
#   SPLIT = False	


  








