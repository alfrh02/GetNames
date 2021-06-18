#!/usr/bin/env python3
import argparse
import random
import os

parser = argparse.ArgumentParser(description="Randomly pick a name from a text file in the output folder of the GetNames.py script. \nExample: 'greek' will locate the 'greek.txt' file in the output folder.")
parser.add_argument("Text", type=str, help="<Required> Text file from which a name will be pulled.")
args = parser.parse_args()

directory = args.Text

if "output" not in directory:
    output = "/output"
else:
    output = ""

if ".txt" not in directory:
    directory = f"{os.getcwd()}{output}/{directory}.txt"
else:
    directory = f"{os.getcwd()}{output}/{directory}"

print("Opening text file...")
try:
    textFile = open(directory, "r")
except FileNotFoundError:
    print(f"File not recognised. Does the file at {directory} exist?")
    exit()

names = textFile.readlines()

textFile.close()

randomLimit = len(names)
rand = random.randint(0,randomLimit - 1)

print(f"\n{names[rand]}")
