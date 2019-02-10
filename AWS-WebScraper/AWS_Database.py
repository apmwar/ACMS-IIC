def addFAQ(fname, question, answer):
    with open(fname, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([question, answer])

import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import csv
import re


myqs = []
answ = []

newq = []
newa = []
"""
count = 1
html = urllib.request.urlopen("https://aws.amazon.com/elasticache/faqs/")
soup = BeautifulSoup(html, 'html.parser')
qs = soup.find_all("div", {"class": "aws-text-box"})
for item in qs:
        if(count > 3 and count < 23):
            i = str(item)
            result2 = i.split("Q:")
            flag = 0
            for j in result2:
                if flag > 1:
                    q = j.split("</b></p>\n")[0]
                    a = j.split("</b></p>\n")[1]
                    myqs.append(q)
                    answ.append(a)
                flag = flag+1
        count = count+1
        print("\n\n")
"""

for i in myqs:
    i = "Q:" + cleanhtml(i)
    newq.append(i)

for j in answ:
    j = cleanhtml(j)
    j = j.replace("A: ", "")
    newa.append(j)


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext    

for (i, j) in zip(newq, newa):
    with open("Amazon ElastiCache.csv", 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([i, j])



