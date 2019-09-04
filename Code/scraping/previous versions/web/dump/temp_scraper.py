# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 22:30:46 2019

@author: Aruna
"""

def addFAQ(fname, question, answer):
    with open(fname, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([question, answer])

import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import csv
import re

# file = pd.read_csv('AWS_Database_Products.csv')

myqs = []
ans = []


    count = 1
# for index, row in file.iterrows():
    html = urllib.request.urlopen("https://aws.amazon.com/elasticache/faqs/")
    soup = BeautifulSoup(html, 'html.parser')
    qs = soup.find_all("div", {"class": "aws-text-box"})
    for item in qs:
        if(count > 3 and count < 23):
            thing = item.find_all("p")
            for j in thing:
                thing = str(j)
                thing = thing.split("Q:")
                flag = 0
                for i in thing:
                    if flag % 2 == 0:
                        print(i)
                        ans.append(i)
                    else:
                        print("Q:", i)
                        print("__________________________")
                        myqs.append("Q:" + i)
                    flag = flag+1
            # print(thing)
        count = count+1
        print("\n\n")
        
# Code below was used to make the CSV file
"""
url = []

for index, row in file.iterrows():
    if row['category'] == 'Database':
        with open('AWS_Database_Products.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([row['name'], row['description'], row['url']])
"""        
        
        qa = item.find_all("p")
        ques = ""
        ans = ""
        for i in qa:
            my_str = str(i)
            if my_str.find("Q:") != -1:
                print("question identified!")
                addFAQ("Amazon ElastiCache.csv", ques, ans)
                my_str = my_str.replace("<p>", "")
                my_str = my_str.replace("</p>", "")
                my_str = my_str.replace("<b>", "")
                my_str = my_str.replace("</b>", "")
                ques = my_str
                ans = ""
            else:
                my_str = my_str.replace("<p>", "")
                my_str = my_str.replace("</p>", "")
                ans = ans + my_str
            print(ques)
            print(ans)
            print("\n")
        # print(qa)
        print("\n\n")
        
        """
        for i in qa:
            qa = str(item)
            ques = qa.split("</b>")[0]
            ques = ques.split("<b>")[1]
            ques = ques.replace("<br/>", "")
            ans = qa.split("</b>")[1]
            ans = ans.replace("<p>", "")
            ans = ans.replace("</p>", "")
            ans = ans.replace("</div>", "")
            ans = ans.replace("<br/>", "")
            print(ques)
            print("__________")
            print(ans)
            print("\n\n")
            # print("processing ", count)
            # addFAQ("Amazon DocumentDB.csv", ques, ans)
            count = count + 1
            """
    
"""
        q = item.find_all("p")[0]
        a = item.find_all("p")[1]
        print(q)
        print(a)
        print("\n\n\n")
        # if q.find("Q.") != -1 or q.find("Q:") != -1:
            # q = q.replace("<b>", "")
            # q = q.replace("</b>", "")
            # addQuestion("Amazon RDS.csv", q)
    
    
"""