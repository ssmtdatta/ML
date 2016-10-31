import json
import numpy as np
import datetime as dt
from timezonefinder import TimezoneFinder
from geopy.distance import vincenty # measures distance between two locations using Vincety's method
import pytz


class SpacetimeDelta():
  """
  Calculates information related to two GPS/time measurements.
  All time functions currently use measurement1's timezone for calculations.
  """

  # accepts 2 dicts that are parsed JSON objects from the data file
  def __init__(self, measurement1, measurement2):

    self.m1 = {'coords' : self._getCoords(measurement1), 'dt' : self._getDatetime(measurement1)}
    self.m2 = {'coords' : self._getCoords(measurement2), 'dt' : self._getDatetime(measurement2)}

  # returns (lat, lng) tuple constructed from measurement
  def _getCoords(self, measurement):
    return (measurement['data']['lat'], measurement['data']['lng'])

  # TODO: ran into issues setting timezone, so right now it is done
  # my adding a timedelta object (timezone_offset) to the datetime
  def _getDatetime(self, measurement):
    timezone_offset = self._getTimezoneOffset(measurement)
    return dt.datetime.utcfromtimestamp(measurement['data']['timestamp'] / 1000) + timezone_offset

  # returns a timedelta object representing the difference between
  def _getTimezoneOffset(self, measurement):
    tf = TimezoneFinder()
    timezone_string = tf.timezone_at(lat=measurement['data']['lat'], lng=measurement['data']['lng'])
    tz = pytz.timezone(timezone_string)
    timestamp = dt.datetime.utcfromtimestamp(measurement['data']['timestamp'] / 1000)
    #in daylight savings transition periods, default to non-DST time
    offset = tz.utcoffset(timestamp, is_dst=False)
    return offset

  # returns absolute value of time difference between the two measurements in seconds
  def time_elapsed(self):
    return abs((self.m1['dt'] - self.m2['dt']).total_seconds())

  # returns distance in meters
  def distance(self):
    return vincenty(self.m1['coords'], self.m2['coords']).meters

  # returns total seconds of weekday time inside the time elapsed
  def weekday_time(self):
    weekdays = [0,1,2,3,4]
    one_day = dt.timedelta(days=1)

    # assign start and end to correct times
    if(self.m1['dt'] <= self.m2['dt']):
      start = self.m1['dt']
      end = self.m2['dt']
    else:
      start = self.m2['dt']
      end = self.m1['dt']

    # return difference if times are on same day
    if(start.date() == end.date()):
      if(start.weekday() in weekdays):
        return self.time_elapsed()
      else:
        return 0

    # otherwise, add up weekend time between two times
    day = start.date()
    day = dt.datetime.combine(day, dt.datetime.min.time())
    counter = dt.timedelta()
    while(True):
      count_it = day.weekday() in weekdays
      if day.date() == start.date():
        counter += (day + one_day - start) * count_it
      elif day.date() == end.date():
        counter += (end - day) * count_it
        break
      else:
        counter += one_day * count_it
      day += one_day
    return counter.total_seconds()

  def weekend_time(self):
    return self.time_elapsed() - self.weekday_time()

  def weekday_time_frac(self):
    return self.weekday_time() / float(self.time_elapsed())

  def weekend_time_frac(self):
    return self.weekend_time() / float(self.time_elapsed())


