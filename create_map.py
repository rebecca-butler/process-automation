import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="Plot addresses from Excel file in Google Maps")
parser.add_argument("file_path", help="Path to Excel file")
args = parser.parse_args()

df = pd.read_excel(args.file_path)
'''print (df.columns[0])
col_one_list = df['Address'].tolist()
print (col_one_list)'''
for i in df.index:
    print (df["Address"][i])