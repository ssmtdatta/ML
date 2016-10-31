import csv
import pandas as pd
import numpy as np
import datetime as dt

# given a current time and cluster, what cluster are you next likely to be in?
def predict_transitions(cluster_ids, local_dt):
  num_clusters = len(set(cluster_ids))

  cluster_transitions = np.zeros((num_clusters, num_clusters), dtype=int)
  for index, cluster in enumerate(cluster_ids):
    if index < len(cluster_ids) - 1:
      next_cluster = cluster_ids[index + 1]
      if cluster != next_cluster:
        cluster_transitions[cluster][next_cluster] += 1

  total = 0
  correct = 0

  num35 = 0
  num44 = 0
  num13 = 0
  for i in cluster_ids:
    if i == 35:
      num35 += 1
    if i == 44:
      num44 += 1
    if i == 13: num13 += 1
  print "NUM 35: ", num35
  print "NUM 44: ", num44
  print "NUM 13: ", num13
  print "RESULT:", sum(cluster_transitions[13])

  for index, cluster in enumerate(cluster_ids):
    if index < len(cluster_ids) - 1:
      next_cluster = cluster_ids[index + 1]
      if cluster != next_cluster:
        if next_cluster == np.argmax(cluster_transitions[cluster]):
          correct += 1
        total += 1

  np.set_printoptions(threshold=np.inf)
  for arr in cluster_transitions:
      if max(arr) > 100: print np.argmax(arr)

  print "Number of Clusters: ", num_clusters
  print "Total: ", total
  print "Correct: ", correct
  print "Accuracy: ", correct / float(total)

if __name__ == '__main__':

  #Read csv data-frame
  #The data is ordered by timestamp and duplicates removed
  usr = 'chris'
  usr_df = pd.read_csv('./'+usr+'_aug_clustered.csv', sep=" ")

  #columns = [id, timestamp, timezone, localdt, lat, lng, avgV, cluster]
  local_dt = usr_df['localdt'].tolist()
  cluster_ids = usr_df['cluster'].tolist()
  # predict_transitions(cluster_ids, local_dt)
  predict_transitions(cluster_ids, local_dt)

