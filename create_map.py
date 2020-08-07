import os
import argparse
import pandas as pd
import gmplot
import http.server
import socketserver

parser = argparse.ArgumentParser(description="Plot addresses from Excel file in Google Maps")
parser.add_argument("file_path", help="Path to Excel file")
args = parser.parse_args()

apikey = 'AIzaSyCxK71WdY85AfLFlP1VJlJyXfyKGd84HhI'

df = pd.read_excel(args.file_path)

# Convert addresses to lat/long
lats = []
longs = []
for i in df.index:
    addr = df["Address"][i]
    city = df["City"][i]
    province = df["State"][i]
    geocode = gmplot.GoogleMapPlotter.geocode('{}, {}, {}'.format(addr, city, province), apikey=apikey)
    lats.append(geocode[0])
    longs.append(geocode[1])


# Set center of map and zoom level
gmap = gmplot.GoogleMapPlotter(43.5503, -79.6914, 9, apikey=apikey)

# Plot locations and draw
gmap.scatter(lats, longs, "red", size = 10, apikey=apikey)
gmap.draw("map.html")

# Start server
port = 8888
handler = http.server.SimpleHTTPRequestHandler
print("Serving at port: " + str(port))
with socketserver.TCPServer(("", port), handler) as httpd:
    httpd.serve_forever()