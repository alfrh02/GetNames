#!/usr/bin/env python3
from urllib.request import urlopen
from bs4 import BeautifulSoup
import fileinput
import argparse
import os
import re

########
#config#
########

pageNumberLimit = 6
# when using behindthename.com, the script will download pages 1-10 (by default) of the given name.

#######
parser = argparse.ArgumentParser(description="Generate a list of names from behindthename.com.")
parser.add_argument("URL", type=str, help="A behindthename.com URL link")
args = parser.parse_args()

url = args.URL
depositFolder = os.getcwd()
depositFolder = depositFolder + "/output"

try:
    os.mkdir("output")
    print("Generating output folder...")
except FileExistsError:
    print("Output folder already exists.")

behindthename = "behindthename.com" in url

pageNumber = 2

if pageNumberLimit == 2: 
    print("Contacting website...")
else:
    print(f"Contacting website page 1/{pageNumberLimit}")
def getHTML(url):
    with urlopen(url) as webpage:
        global source
        source = webpage.read().decode()

getHTML(url)

if behindthename:
    depositFileName = url.split("/")
    depositFileName = depositFileName[-1]
    if "masculine" in url:
        depositFileName = f"{depositFileName}-masculine" 
    if "feminine" in url:
        depositFileName = f"{depositFileName}-feminine"
    if "unisex" in url:
        depositFileName = f"{depositFileName}-unisex"
else:
    depositFileName = url.split("/")
    depositFileName = depositFileName[1].split("/")
    depositFileName = depositFileName[0]

directory = f"{depositFolder}/{depositFileName}.html"

directoryTxt = f"{depositFolder}/{depositFileName}.txt"

#creating .html file for the source html to be deposited into
if os.path.exists(directory):
    print("Deposit file already exists.")

    os.remove(directory)
    print("Previous deposit file removed.")
    
    depositFile = open(directory, "w")
    depositFile.write(source)
#depositing the source html
else:
    depositFile = open(directory, "w")
    depositFile.write(source)

printPageLimit = pageNumberLimit - 1

if behindthename:
    while pageNumber != pageNumberLimit:
        url = f"{url}/{pageNumber}"
        print(f"Contacting website page {pageNumber}/{printPageLimit}")
        getHTML(url)
        depositFile.write(source)
        pageNumber = pageNumber + 1
        

print(f"Source HTML deposited at {directory}")

#parsing the html
if behindthename:
    htmlFile = open(directory)
    soup = BeautifulSoup(htmlFile, 'html.parser')
    findClassNgl = soup.find_all("a", class_="nll")
    reformedHtml = str(findClassNgl)
    #print(reformedHtml)

    os.remove(directory)
    htmlFile = open(directory, "w")
    htmlFile.close()
    htmlFile = open(directory, "r+")
    htmlFile.write(reformedHtml)
    htmlFile.close()
    htmlFile = open(directory)

    soup = BeautifulSoup(htmlFile, 'html.parser')
    reformedHtml = soup.get_text()

    os.remove(directory)
    htmlFile = open(directory, "w")
    htmlFile = open(directory, "r+")
    htmlFile.write(reformedHtml)
        
    htmlFile.close()

    print(f"Parsed HTML deposited at {directory}")
    
    names = reformedHtml
    names = names.split(",")

    file = open(directoryTxt, "w")
    for name in names:
        file.write(f"{name}\n")
    print(".txt file created with list of names")
    file.close()
    os.remove(directory)
    print(f"Parsed HTML file removed at {directory}")
  
    def replace(filePath, text, subs, flags=0):
        with open(directoryTxt, "r+") as file:
            file_contents = file.read()
            text_pattern = re.compile(re.escape(text), flags)
            file_contents = text_pattern.sub(subs, file_contents)
            file.seek(0)
            file.truncate()
            file.write(file_contents)
    subs = ""

    text="["
    replace(directoryTxt, text, subs)

    text=" "
    replace(directoryTxt, text, subs)

    text="]"
    replace(directoryTxt, text, subs)

    text="1"
    replace(directoryTxt, text, subs)

    text="2"
    replace(directoryTxt, text, subs)

    text="3"
    replace(directoryTxt, text, subs)

    print("Dodgy characters removed.")
    print(f"Process complete. List of names can be found at {directoryTxt}")
