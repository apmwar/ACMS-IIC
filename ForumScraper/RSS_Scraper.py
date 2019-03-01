# Importing the necessary libraries
import csv
import requests
import xml.etree.ElementTree as ET

def loadRSS():
    
    # url of rss feed 
    url = 'https://forums.aws.amazon.com/rss/rssmessages.jspa?threadID=298153'
  
    # creating HTTP response object from given url 
    resp = requests.get(url) 
  
    # saving the xml file 
    with open('rssfeed.xml', 'wb') as f: 
        f.write(resp.content) 
        
        


    # create element tree object 
    tree = ET.parse("rssfeed.xml") 
  
    # get root element 
    root = tree.getroot() 
  
    # create empty list for news items 
    feed = [] 
  
    # iterate news items 
    for item in root.findall('./channel/item'): 
  
        # empty news dictionary 
        news = {} 
  
        # iterate child elements of item 
        for child in item: 
  
            # special checking for namespace object content:media 
            if child.tag == '{http://search.yahoo.com/mrss/}content': 
                news['media'] = child.attrib['url'] 
            else: 
                news[child.tag] = child.text.encode('utf8') 
  
        # append news dictionary to news items list 
        feed.append(news) 
      