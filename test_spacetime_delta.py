import unittest
import spacetime_delta as s
import datetime as dt

class TestWeekdayTime(unittest.TestCase):

    def setUp(self):
       offset = dt.timedelta(hours = 5) # time offset at (55, 55) (in Russia)
       self.epoch = dt.datetime(1970,1,1) + dt.timedelta(hours=5)

    # Sep 1, 2016 is a Thursday
    def test_inside_one_day(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 6, 30) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 15, 15) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 8.75)

    def test_inside_one_day_reverse(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 15, 15) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 6, 30) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 8.75)

    def test_across_one_day(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 23) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 2, 1) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 2)

    def test_one_weekday(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 0) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 2, 0) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 24)

    def test_one_week(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 0) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 8, 0) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 120)

    def test_across_multiple_weeks_starting_in_weekday(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 6) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 20, 1) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 307)

    def test_across_multiple_weeks_starting_in_weekend(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 3, 6) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 19, 13) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 2*5*24 + 13)

    def test_inside_weekend(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 3, 5) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 4, 12) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 0)

    def test_starting_inside_weekend(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 3, 5) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 5, 20) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 20)



class TestOtherMethods(unittest.TestCase):

    def setUp(self):
       self.epoch = dt.datetime(1970,1,1) + dt.timedelta(hours=5)

    # Sep 1, 2016 is a Thursday
    def test_weekday_time(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 6, 30) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1, 15, 15) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time() / 3600, 8.75)

    def test_weekday_time_frac(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 8) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekday_time_frac(), float(5)/7)

    def test_weekend_time_frac(self):
        m1 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 1) - self.epoch).total_seconds() * 1000}}
        m2 = {'data' : {'lat': 55, 'lng': 55, 'timestamp': (dt.datetime(2016, 9, 8) - self.epoch).total_seconds() * 1000}}
        std = s.SpacetimeDelta(m1, m2)
        self.assertEqual(std.weekend_time_frac(), float(2)/7)



if __name__ == '__main__':
    unittest.main()
