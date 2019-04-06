# First we import the libraries
import urllib.request
from bs4 import BeautifulSoup
import csv

# Load up the target page URL
url = 'https://aws.amazon.com/'

# Load up the instance of the urllib object to target page
html_data = urllib.request.urlopen(url)

# Encode HTML to the beautiful soup object
soup = BeautifulSoup(html_data, 'html.parser')

# Store the data of that div that contains the following class name
name = []
url = []
description = []

# Extracting features (name, URL and description) of each product

for target_div in soup.find_all("div", {"class": "lb-content-item"}):
    
    # Extract the FAQ page URL
    my_str = str(target_div)
    my_str = my_str.split('href="')[1]
    my_str = my_str.split('/')[1]
    url.append("https://aws.amazon.com/" + my_str + "/faqs")
    
    # Extract the product name
    new_str = str(target_div)
    new_str = new_str.split("<span>")[0]
    new_str = new_str.split('"> ')[1]
    name.append(new_str)
    
    # Extract the description
    for j in target_div.find("span"):
        description.append(j)
        
    # And finally insert it as a row in the CSV file
    with open('AWS_Products.csv', 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([name[-1], description[-1], url[-1]])