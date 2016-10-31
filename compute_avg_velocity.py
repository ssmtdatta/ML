import csv
import pandas as pd
import numpy as np
import haversine_distance as hv


def averageVelocity(w, timestamps, lats, lngs): 

  window = w * 60000. 
  delta_t = 2 * window	

  avg_velocity = [0]  # ==> pad the boundary by zero or assume instantaneous velocity

  for t in range(1, len(timestamps)-1):
    # start with the second point in the sequence	
    # center the window at this point

    stamp = timestamps[t]        # timestamp of the center point
    prev_stamp = stamp - window  # expected timestamp at the start of the window
    next_stamp = stamp + window  # expected timestamp at the end of the window
  
    # if the starting boundary of the window falls outside the start of the sequence, 
    # assume the first point is the previous location
    if prev_stamp < timestamps[t-1]:
      prev_loc = (lats[t-1], lngs[t-1])
    # check if there are points at or before the start of the window 
    else:
      indexes = np.where( (timestamps <= prev_stamp) )[0]
      prev_idx = indexes[-1]
      prev_loc = (lats[prev_idx], lngs[prev_idx])

    # check if there is a point at the end boundary of the window 
    next_idx = np.where( timestamps >= next_stamp )[0] # ==> allow offset??
    if next_idx.any():
      next_loc = (lats[next_idx[0]], lngs[next_idx[0]])
    else:
  	  next_loc = ( lats[t], lngs[t] )

    dist = hv.haversineDistance(prev_loc, next_loc)
  
    avg_velocity.append(round(dist/(delta_t/1000), 6)) # [meter/sec]

  avg_velocity.append(avg_velocity[-1]) # ==> pad the boundary by zero or assume previous velocity
  avg_velocity[0] = avg_velocity[1]
  
  return avg_velocity


#--------------------------------
# main()
#

#Read data
PATH = '/Users/susmitadatta/Jio/Jiobit/Data/Aug2016/'
# read csv data, order by timestamp and remove duplicates
#usr = 'chris'
usr = 'alex'
usr_df = pd.read_csv(PATH+usr+'_aug.csv', sep=" ")
usr_df = usr_df.drop_duplicates(['timestamp'])
usr_df = usr_df.sort_values(by='timestamp', ascending=True)
usr_df = usr_df.reset_index(drop=True)
#
timestamps = np.array(usr_df['timestamp'])
lats = np.array(usr_df['lat'])
lngs = np.array(usr_df['lng'])
print(len(usr_df))

# half window
w = 1.5
avg_velocity = averageVelocity(w, timestamps, lats, lngs)

usr_df['avgV'] = avg_velocity

usr_df.to_csv(PATH+usr+'_aug_avgV.csv', sep=" ", float_format='%.6f', mode = 'w', index=False)

