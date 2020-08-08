import os
import json
import argparse
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import gmplot
from geopy.distance import geodesic
import http.server
import socketserver

parser = argparse.ArgumentParser(description="Cluster addresses by proximity")
parser.add_argument("apikey", nargs="?", help="Google Maps API key")
parser.add_argument("file_path", nargs="?", help="Path to Excel file (if not provided, stored JSON will be used)")
parser.add_argument("-map", action="store_true", help="Optional flag to plot locations on map and serve")
args = parser.parse_args()

api_key = args.apikey

# If Excel file is given, convert addresses to lat/long
if args.file_path and args.apikey:
    print("Geocoding addresses...")
    df = pd.read_excel(args.file_path)
    locations = []
    for i in df.index:
        name = df["Account"][i]
        addr = df["Address"][i]
        city = df["City"][i]
        province = df["State"][i]
        try:
            location = gmplot.GoogleMapPlotter.geocode("{}, {}, {}".format(addr, city, province), apikey=api_key)
            location_obj = {
                "name": name,
                "address": addr,
                "city": city,
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

# Organize into data frame
df = pd.DataFrame(location_data)
cols = list(df)
cols.insert(0, cols.pop(cols.index("city")))
cols.insert(0, cols.pop(cols.index("address")))
cols.insert(0, cols.pop(cols.index("name")))
df = df.loc[:, cols]

# Split locations into set of clusters using k-means clustering algorithm
print("Clustering...")
num_clusters = 15
kmeans = KMeans(n_clusters=num_clusters, init="k-means++")
kmeans.fit(df[df.columns[3:5]])
df["cluster_label"] = kmeans.fit_predict(df[df.columns[3:5]])
centers = kmeans.cluster_centers_
labels = kmeans.predict(df[df.columns[3:5]])

# Output clusters to text file
df = df.sort_values("cluster_label")
with open("clusters.txt", "w") as txt_file:
    for i in range(num_clusters):
        txt_file.write("\nCluster {}:\n".format(i))
        for index, row in df.iterrows():
            if row["cluster_label"] == i:
                txt_file.write("{}, {}, {}\n".format(row["name"], row["address"], row["city"]))

# If map flag is set, create map and serve
if args.map and args.apikey:
    print("Mapping...")
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