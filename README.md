# README (updated 8/26/16)

##Setup
Install the required libraries using pip.

Both files require that the directory containing the august data is named **data** and is located in the jio-machine-learning directory. The .gitignore file in the root is set to ignore that file so it isn't stored on github, so you'll have to move it there yourself.

## What each file does
1) **coordinate_frequencies.py**: This program calculates how many times each GPS coordinate ( a (lat, long) tuple rounded to a certain precision) appears.

2) **plot_gps_data.py**: This program currently plots all the GPS points of a certain user on a map. It creates a mymap.html file which you can then open to view the map.
