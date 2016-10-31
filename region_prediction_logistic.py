# classifiction.py
import csv
import pandas as pd
import numpy as np
# Datetime
import datetime as dt
from datetime import datetime
# Logistic Regression
from sklearn import datasets
from sklearn import metrics
from sklearn import cross_validation
from sklearn.linear_model import LogisticRegression


def predict_region(input_weekday, input_hour, input_minute):

  #Read data
  path = './'
  filename = 'alex_aug_clustered.csv'


  df = pd.read_csv(path+filename, sep=" ")
  # [col: id timestamp timezone localdt lat lng avgV timediff cluster]

  # training labels
  cluster_id = np.array(df['cluster'])  #cluster ID for each record

  # training features
  localdt = df['localdt'].tolist()
  # extract hour, minute, day of the week from datetime srting in the dats (col:'localdt')
  hour = []
  minute = []
  wkday = []
  sin_time = []
  for d in localdt:
    local_dt = d[:19]
    dt_ = dt.datetime.strptime(local_dt, "%Y-%m-%d %H:%M:%S")
    hr = dt_.hour
    mn = dt_.minute
    wkd = dt_.weekday()
    hour.append(hr)
    minute.append(mn)
    wkday.append(wkd)

  # feature matrix
  features =  np.column_stack((hour, minute, wkday))


  # logistic regression
  X = features     # features
  Y = cluster_id   # labels
  # fit a logistic regression model to the data

  model = LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
            intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=10,
            penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
            verbose=0, warm_start=False)

  model.fit(X, Y)
  f = [[input_hour, input_minute, input_weekday]]
  predicted = model.predict(X)
  print len(predicted)
  # print Y

if __name__ == '__main__':
  np.set_printoptions(threshold=np.inf)
  weekday = 0
  hour = 13
  minute = 30
  predict_region(weekday, hour, minute)



