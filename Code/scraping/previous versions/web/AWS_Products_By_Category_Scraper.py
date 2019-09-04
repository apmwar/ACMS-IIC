# First we import the libraries
import urllib.request
from bs4 import BeautifulSoup
import csv

# Load up the target page URL
url = 'https://aws.amazon.com/products'

# Load up the instance of the urllib object to target page
html_data = urllib.request.urlopen(url)

# Encode HTML to the beautiful soup object
soup = BeautifulSoup(html_data, 'html.parser')
soup.prettify()

# Store the data of that div that contains the following class name
category = []
name = []
description = []
isFAQAvailable = []
url = []

isValidURL = []

# Extracting the categories of all products
for target_div in soup.find_all("div", {"class": "lb-item-wrapper"}):
    
    # Start by extracting the category from the target_div
    cat = str(target_div.find_all("span")[0])
    cat = cat.replace("&amp;", "&")
    cat = cat.replace("<span>", "")
    cat = cat.replace("</span>", "")
    
    
    # Extracting features (category, name, description and URL) of each product
    
    for item in target_div.find_all("div", {"class", "lb-content-item"}):
        # print(item)
        
        # Extract the name of the product
        my_str = str(item)
        my_str = my_str.split("<span>")[0]
        my_str = my_str.split('"> ')[1]
        name.append(my_str)
        
        # Extract the product description
        for my_str in item.find("span"):
            description.append(my_str)
        
        # Extract the FAQ page URL
        my_str = str(item)
        my_str = my_str.split('href="')[1]
        my_str = my_str.split('/')[1]
        
        # First find out if the specified URL is valid or not
        
        product_url = "https://aws.amazon.com/" + my_str
        product_data = urllib.request.urlopen(product_url)
        product_soup = BeautifulSoup(product_data, 'html.parser')
        product_soup.prettify()
        found = str(product_soup).split('data-lb-page-path="')[1]
        print(found)
        
        # If valid then append to the url
        url.append("https://aws.amazon.com/" + my_str + "/faqs")
        
        # Add the category as well
        category.append(cat)

        # Finally, adding the resultant data to the CSV file
        with open('AWS_Products_By_Category.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([category[-1], name[-1], description[-1], url[-1]])
