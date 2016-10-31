## Spark Application - execute with spark-submit

## Imports
from pyspark import SparkConf, SparkContext
import json
import csv
import pickle
import collections
import datetime as dt
from timezonefinder import TimezoneFinder
import pytz



## Module constants and global variables
APP_NAME = 'Spark App'

INPUT_PATH = '/Users/susmitadatta/Jio/Jiobit/S3sync/Aug2016/*/*/'
INPUT_FILETYPE = '*.gz'

OUTPUT_PATH = '/Users/susmitadatta/Jio/Jiobit/Data/Aug2016/'
#OUTPUT_FILE = 'aug2016'



global PRECISION   # for lat and lng decimal places
PRECISION = 6      



## Functions
def parse(line):
  '''
  Parses a json string and returns keys and values
  '''
  parsed = {'device_id' : str(line['data']['device_id']), \
  'timestamp' : int(line['data']['timestamp']), \
  'lat': float(line['data']['lat']), \
  'lng': float(line['data']['lng'])}
  return parsed


def complete_json(line):
  '''
  Ensures that each line is a valid and complete line of json
  '''
  if not type(line) == dict: return false
  if not 'data' in line: return false

  data = line['data']
  return 'device_id' in data and \
         'timestamp' in data and \
         'lat' in data and \
         'lng' in data


def parse_files(file_contents):
  '''
  Parses json, removes incomplete hashes
  '''
  decoded_json = file_contents.map(json.loads)
  return decoded_json.filter(complete_json).map(parse).map(add_timezone_info)


def add_timezone_info(data):
  data['timezone'] = get_timezone(data)
  data['local_datetime'] = get_local_datetime(data)
  return data

def get_timezone(data):
  tf = TimezoneFinder()
  timezone_string = tf.timezone_at(lat=data['lat'], lng=data['lng'])
  return timezone_string

# returns a timedelta object representing the difference between
def get_local_datetime(data):
  tf = TimezoneFinder()
  timezone_string = tf.timezone_at(lat=data['lat'], lng=data['lng'])
  tz = pytz.timezone(timezone_string)
  data_dt = dt.datetime.utcfromtimestamp(data['timestamp'] / 1000) #date time in utc
  #in daylight savings transition periods, default to non-DST time
  offset = tz.utcoffset(data_dt, is_dst=False) # offset compared to a given timezone
  return data_dt + offset

  
def write_txtfile(rdd):
  data = rdd.collect()
  for s in range(0,len(data)):
    print(data[s]['device_id'])
  
  with open(OUTPUT_PATH+OUTPUT_FILE+'txt', 'w') as f:
    for s in range(0,len(data)):   
      f.write( '%-1s %-1d %-1.6f %-1.6f \n' \
      % (data[s]['device_id'],\
        data[s]['timestamp'], \
        round(data[s]['lat'], PRECISION),\
        round(data[s]['lng'], PRECISION) ))
  f.close()


def createOrderedDict(line):
  #return an ordered dictionary
  ordered_line = collections.OrderedDict()
  ordered_line['id'] = str(line['device_id'])
  ordered_line['timestamp'] = int(line['timestamp'])
  ordered_line['timezone'] = line['timezone']
  ordered_line['localdt'] = line['local_datetime']
  ordered_line['lat'] = round(float(line['lat']), 6) 
  ordered_line['lng'] = round(float(line['lng']), 6)

  return ordered_line

def write_csvfile(rdd, filename):
  listOfDict = rdd.collect()
  # list of ordered dictionaries
  ordered = []       
  for k in range(0,len(listOfDict)):
        ordered.append(createOrderedDict(listOfDict[k]))

  keys = ordered[0].keys()
  with open(OUTPUT_PATH+filename+'.csv', 'w') as f:
    dict_writer = csv.DictWriter(f, keys, delimiter =' ')
    dict_writer.writeheader()
    dict_writer.writerows(ordered)    


def save_as_dictionary(rdd, filename):
  listOfDict = rdd.collect()
  pickle.dump( listOfDict, open(OUTPUT_PATH+filename+'.p', 'wb' ) )  


   
## Main functionality
def main(sc):
  file_contents = sc.textFile(INPUT_PATH+INPUT_FILETYPE)
  file_contents.persist()
  rdd_data = parse_files(file_contents) 


  ## list of distinct device ids
  # device_ids = data.map(lambda x: x['device_id']).distinct().collect()

  ## create dict of device_ids to RDDs, where each RDD has data from that device_id
  # device_data_dict = {device_id : data.filter(lambda x: x['device_id'] == device_id) for device_id in device_ids}

  
  ## ==> save data <==

  # data for a usr 
  device_id = '18476682571' # Chris
  rdd_device_data = rdd_data.filter(lambda x: x['device_id'] == device_id)

  #device_id = '14084319342' # Alex 
  #rdd_device_data = rdd_data.filter(lambda x: x['device_id'] == device_id)
  

  ## save data as list of dictionaries 
  save_as_dictionary(rdd_device_data, filename="chris_aug")

  ## save data as csv
  write_csvfile(rdd_device_data, filename="chris_aug")


  



## Spark driver
if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)

    main(sc)

