import os
import argparse
import pandas as pd
import gmplot

parser = argparse.ArgumentParser(description="Plot addresses from Excel file in Google Maps")
parser.add_argument("file_path", help="Path to Excel file")
args = parser.parse_args()

apikey = 'AIzaSyCxK71WdY85AfLFlP1VJlJyXfyKGd84HhI'

df = pd.read_excel(args.file_path)

# Convert address to lat/long and plot
for i in df.index:
    addr = df["Address"][i]
    city = df["City"][i]
    province = df["State"][i]
    geocode = gmplot.GoogleMapPlotter.geocode('{}, {}, {}'.format(addr, city, province), apikey=apikey)
    gmap = gmplot.GoogleMapPlotter(geocode[0], geocode[1], 13, apikey=apikey)
    break

# Draw the map:
gmap.draw('map.html')