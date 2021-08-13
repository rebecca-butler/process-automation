# process-automation

Scripts for automating boring tasks.

## class_schedule_checker

This script checks the University of Waterloo class schedule to see if there are any seats available for a given class.
Run this instead of checking manually every 30 minutes!

Dependencies: `bs4`, `lxml`, `requests_html`, `smtplib`

Script usage: `python3 form_extractor.py`

Follow the prompts to enter the subject, course number, section number, and term.
If you would like to receive an email alert when a spot opens up, you must also enter your email and password.
Note: this tool is designed to work with gmail accounts. 

## cluster_addresses

This script clusters addresses in a given Excel file based on proximity.
The first time the script is run, the Excel file must be passed in as an argument along with a Google Maps API key to geocode the addresses.
The latitude and longitude values will be then stored in a JSON file so the script can be be run without the API key.

The `-map` flag is optional. If used, it will create an http server at `localhost:8888/map.html` to show the map with a visualization of the clusters.

If the `-map` flag is not used, the script will output a `clusters.txt` file containing 15 address clusters.

Dependencies: `argparse`, `pandas`, `sklearn`, `gmplot`, `xlrd`

Script usage: `python3 create_map.py <api_key> <file_path> [-map]`
