# cluster_addresses.py

This script clusters addresses in a given Excel file based on proximity. The first time the script is run, the Excel file must be passed in as an argument along with a Google Maps API key to geocode the addresses. The latitude and longitude values will be then stored in a JSON file so the script can be be run without the API key.

The `-map` flag is optional. If used, it will create an http server at `localhost:8888/map.html` to show the map with a visualization of the clusters.

If the `-map` flag is not used, the script will output a `clusters.txt` file containing 15 address clusters.

Run the following command to install needed dependencies:
`pip install argparse pandas sklearn gmplot xlrd`

Script usage: `python create_map.py <api_key> <file_path> [-map]`