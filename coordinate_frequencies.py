## Spark Application - execute with spark-submit
## bin/spark-submit jiobit/sparkCodes/device_log.py

## Imports
from pyspark import SparkConf, SparkContext
import json
import datetime as dt
from timezonefinder import TimezoneFinder
import pytz


## Module constants and global variables
APP_NAME = 'Spark App'
INPUT_PATH = './data/15/*/'
INPUT_FILETYPE = '*.gz'


## Closure Functions
def parse(line):
  '''
  Parses a json string and returns keys and values
  '''
  parsed = {'device_id' : str(line['data']['device_id']), \
  'timestamp' : int(line['data']['timestamp']), \
  'lat': float(line['data']['lat']), \
  'lng': float(line['data']['lng'])}
  return parsed

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

# ensures each line is a valid and complete line of json
def complete_json(line):
  if not type(line) == dict: return false
  if not 'data' in line: return false

  data = line['data']
  return 'device_id' in data and \
         'timestamp' in data and \
         'lat' in data and \
         'lng' in data

# Parses json, removes incomplete hashes
def parse_files(file_contents):
  decoded_json = file_contents.map(json.loads)
  return decoded_json.filter(complete_json).map(parse).map(add_timezone_info)

# accepts RDD of parsed data (with device_id, timestamp, lat, and lng)
# returns rdd of (coord, frequency) with corods accurate to precision specified
def coord_frequency(data, precision=5):
  coords = data.map(lambda x: ((round(x['lat'], precision), round(x['lng'], precision)), 1))
  coordsFreq = coords.reduceByKey(lambda x, y: x+y)
  coordsFreq = coordsFreq.sortBy(lambda x: x[1], ascending=False)
  return coordsFreq

## Main functionality
def main(sc):
  file_contents = sc.textFile(INPUT_PATH+INPUT_FILETYPE)
  file_contents.persist()
  data = parse_files(file_contents)

  # list of distinct device ids
  device_ids = data.map(lambda x: x['device_id']).distinct().collect()

  # create dict of device_ids to RDDs, where each RDD has data from that device_id
  device_data_dict = {device_id : data.filter(lambda x: x['device_id'] == device_id) for device_id in device_ids}

  coordsFreq = coord_frequency(device_data_dict['14084319342'], precision=4)

  print "data: ", data.take(5) , "\n"
  print "coordinate frequencies:", coordsFreq.take(5)


## Spark driver
if __name__ == "__main__":
    # Configure Spark
    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc   = SparkContext(conf=conf)

    main(sc)
