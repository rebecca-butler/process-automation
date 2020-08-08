import os
import json
import argparse
import pandas as pd
import gmplot
import http.server
import socketserver
from geopy.distance import geodesic

parser = argparse.ArgumentParser(description="Cluster addresses in 10km radius")
parser.add_argument("apikey", nargs="?", help="Google Maps API key")
parser.add_argument("file_path", nargs="?", help="Path to Excel file (if not provided, stored JSON will be used)")
parser.add_argument("-map", action="store_true", help="Optional flag to plot locations on map and serve")
args = parser.parse_args()

api_key = args.apikey

# If Excel file is given, convert addresses to lat/long
if args.file_path and args.apikey:
    df = pd.read_excel(args.file_path)
    locations = []
    for i in df.index:
        addr = df["Address"][i]
        city = df["City"][i]
        province = df["State"][i]
        try:
            location = gmplot.GoogleMapPlotter.geocode("{}, {}, {}".format(addr, city, province), apikey=api_key)
            location_obj = {
                "name": df["Account"][i],
                "lat": location[0],
                "long": location[1]
            }
            locations.append(location_obj)
        except:
            print(addr + " failed")

    # Store locations in JSON file
    with open("locations.json", "w") as outfile:
        json_string = json.dumps(locations, indent=4, sort_keys=True, separators=(',', ': '))
        outfile.write(json_string)

# Retrieve locations from JSON file
with open("locations.json") as json_file:
    location_data = json.load(json_file)

# If map flag is set, create map and serve
if args.map and args.apikey:
    # Set center of map and zoom level
    gmap = gmplot.GoogleMapPlotter(43.5503, -79.6914, 9, apikey=args.apikey)

    # Plot locations and draw
    lats = []
    longs = []
    for location in location_data:
        lats.append(location["lat"])
        longs.append(location["long"])
    gmap.scatter(lats, longs, "red", size = 10, apikey=args.apikey)
    gmap.draw("map.html")

    # Start server
    port = 8080
    handler = http.server.SimpleHTTPRequestHandler
    print("Serving at port: " + str(port))
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# Split locations into set of clusters such that two points within 10km of each other will be in the same cluster

#print(geodesic(location[0], location[1]).kilometers)