import csv
import pandas as pd
import numpy as np
import datetime as dt

# given a current time and cluster, what cluster are you next likely to be in?
def predict_transitions(cluster_ids, local_dt):
  num_clusters = len(set(cluster_ids))

  threshold = len(cluster_ids) * 8 / 10
  print "THRESHOLD: ", threshold

  cluster_transitions = np.zeros((24, num_clusters, num_clusters), dtype=int)
  for index, cluster in enumerate(cluster_ids):
    if index < threshold and index < len(cluster_ids) - 1:
      next_cluster = cluster_ids[index + 1]

      dt_ = dt.datetime.strptime(local_dt[index][:19], "%Y-%m-%d %H:%M:%S")
      hour = dt_.hour
      hour = 0 # delete this to use hourly information
      if cluster != next_cluster:
        cluster_transitions[hour][cluster][next_cluster] += 1

  total = 0
  correct = 0
  for index, cluster in enumerate(cluster_ids):
    if index > threshold and index < len(cluster_ids) - 1:
      next_cluster = cluster_ids[index + 1]
      dt_ = dt.datetime.strptime(local_dt[index][:19], "%Y-%m-%d %H:%M:%S")
      hour = dt_.hour
      hour = 0 # delete this to use hourly information
      if cluster != next_cluster:
        if next_cluster == np.argmax(cluster_transitions[hour][cluster]):
          correct += 1
        total += 1

  np.set_printoptions(threshold=np.inf)
  print cluster_transitions[0]

  print "Total: ", total
  print "Correct: ", correct
  print "Accuracy: ", correct / float(total)

# Given a time of day and weekday, what cluster are you likely to be in?
def predict_regions(cluster_ids, local_dt):
  num_clusters = len(set(cluster_ids))
  threshold = len(cluster_ids) * 9 / 10
  print "THRESHOLD: ", threshold

  region_frequencies = np.zeros((7, 24, num_clusters), dtype=int)
  for index, cluster in enumerate(cluster_ids):
    if index < threshold and index < len(cluster_ids):
      dt_ = dt.datetime.strptime(local_dt[index][:19], "%Y-%m-%d %H:%M:%S")
      hour = dt_.hour
      weekday = dt_.weekday()

      region_frequencies[weekday][hour][cluster] += 1

  total = 0
  correct = 0
  for index, cluster in enumerate(cluster_ids):
    if index > threshold and index < len(cluster_ids) - 1:
      dt_ = dt.datetime.strptime(local_dt[index][:19], "%Y-%m-%d %H:%M:%S")
      hour = dt_.hour
      weekday = dt_.weekday()
      if cluster == np.argmax(region_frequencies[weekday][hour]):
        correct += 1
      total += 1

  np.set_printoptions(threshold=np.inf)
  print region_frequencies

  print "Total: ", total
  print "Correct: ", correct
  print "Accuracy: ", correct / float(total)

if __name__ == '__main__':

  #Read csv data-frame
  #The data is ordered by timestamp and duplicates removed
  usr = 'alex'
  usr_df = pd.read_csv('./'+usr+'_aug_clustered.csv', sep=" ")

  #columns = [id, timestamp, timezone, localdt, lat, lng, avgV, cluster]
  local_dt = usr_df['localdt'].tolist()
  cluster_ids = usr_df['cluster'].tolist()
  # predict_transitions(cluster_ids, local_dt)
  predict_regions(cluster_ids, local_dt)

