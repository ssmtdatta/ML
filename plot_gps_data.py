import json
import numpy as np
import gmplot

from pyspark import  SparkContext
sc = SparkContext( 'local', 'pyspark')

dev_id = '18476682571'

filename = "./data/*/*/*.gz"

lines = sc.textFile(filename)
data = lines.map(lambda line: json.loads(line))

# print data.take(5)
data = data.filter(lambda item: 'data' in item and 'device_id' in item['data'])
user_data = data.filter(lambda item: item['data']['device_id'] == dev_id)

arr = user_data.collect()
print len(arr)

# print arr
lats = [e['data']['lat'] for e in arr]
lngs = [e['data']['lng'] for e in arr]

gmap = gmplot.GoogleMapPlotter.from_geocode("Chicago", 12)
gmap.scatter(lats, lngs, '#3B0B39', size=40, marker=False) # basic scatterplot

# gmap.plot(lats, lngs, 'cornflowerblue', edge_width=10) # plot with lines connecting consecutive points
# gmap.scatter(lats, lngs, 'k', marker=True) # scatterplot with location marker
# gmap.heatmap(lats, lngs, 10)

gmap.draw("mymap.html")


