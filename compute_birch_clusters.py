from sklearn.cluster import Birch
import pandas as pd
import csv
import numpy as np




def birch(X):
  brc = Birch(branching_factor=20, n_clusters=None, threshold=0.001, compute_labels=True)
  birch_model = brc.fit(X)
  labels = birch_model.labels_
  centroids = birch_model.subcluster_centers_
  n_clusters = np.unique(labels).size
  
  return labels, centroids, n_clusters



#Read data
PATH = '/Users/susmitadatta/Jio/Jiobit/Data/Aug2016/'
# read csv data, order by timestamp and remove duplicates
#usr = 'chris'
usr = 'alex'
usr_df = pd.read_csv(PATH+usr+'_aug_avgV.csv', sep=" ")


v_thresh = 3
#
df_thresh = usr_df.loc[ (usr_df['avgV'] <= v_thresh) ]

df_thresh_lats = df_thresh['lat'].tolist()
df_thresh_lngs = df_thresh['lng'].tolist()



X = []
for i in range(0, len(df_thresh_lats)):
  coords = [ df_thresh_lats[i], df_thresh_lngs[i] ]
  X.append(coords)


labels, centroids, n_clusters = birch(X)
print(n_clusters)
#cnt_lats = centroids[:, 0]
#cnt_lngs = centroids[:, 1]
df_thresh['cluster'] = labels
df_thresh.to_csv(PATH+usr+'_aug_clustered.csv', sep=" ", float_format='%.6f', mode = 'w', index=False)


