import os
import json
import argparse
import pandas as pd
import gmplot
import http.server
import socketserver
import time
from geopy.geocoders import Nominatim 
from geopy.distance import geodesic

parser = argparse.ArgumentParser(description="Plot addresses from Excel file in Google Maps")
parser.add_argument("file_path", help="Path to Excel file")
parser.add_argument("apikey", nargs="?", help="Google Maps API key (optional)")
args = parser.parse_args()

df = pd.read_excel(args.file_path)
'''
# Convert addresses to lat/long
lats = []
longs = []
locations = []
for i in df.index:
    addr = df["Address"][i]
    city = df["City"][i]
    province = df["State"][i]
    geocode = gmplot.GoogleMapPlotter.geocode("{}, {}, {}".format(addr, city, province), apikey=args.apikey)
    time.sleep(1) # sleep between API calls
    lats.append(geocode[0])
    longs.append(geocode[1])
    locations.append(geocode)

# Set center of map and zoom level
gmap = gmplot.GoogleMapPlotter(43.5503, -79.6914, 9, apikey=args.apikey)

# Plot locations and draw
gmap.scatter(lats, longs, "red", size = 10, apikey=args.apikey)
gmap.draw("map.html")

# Start server
port = 8888
handler = http.server.SimpleHTTPRequestHandler
print("Serving at port: " + str(port))
with socketserver.TCPServer(("", port), handler) as httpd:
    httpd.serve_forever()'''

# Convert addresses to lat/long
locations = []
for i in df.index:
    addr = df["Address"][i]
    city = df["City"][i]
    province = df["State"][i]
    geolocator = Nominatim(user_agent="http")
    location = geolocator.geocode("{}, {}, {}".format(addr, city, province))
    try:
        location_obj = {
            "name": df["Account"][i],
            "lat": location.latitude,
            "long": location.longitude
        }
        locations.append(location_obj)
    except:
        print(addr + " failed")

# Store locations
with open("locations.txt", "w") as outfile:
    json_string = json.dumps(locations, indent=4, sort_keys=True, separators=(',', ': '))
    outfile.write(json_string)

# Split locations into set of clusters such that two points within 10km of each other will be in the same cluster

#print(geodesic(location[0], location[1]).kilometers)