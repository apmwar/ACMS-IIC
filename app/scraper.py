# Code to scrape each forumID for SPECIFIC # of threads
# by default, atleast 50 of the most recent threads are scraped

# Importing the necessary libraries first

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time


# Fetch all the messages inside each thread and store it into the final TSV file with tag as the name of the product
# Input: The thread URL and the target file name

def updateNumberOfThreads(fid, forumName):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
    url = "https://forums.aws.amazon.com/forum.jspa?forumID=" + str(fid)
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    soup.prettify()

    numberOfThreads = soup.find_all("nobr")

    temp = str(numberOfThreads[1])
    temp = temp.replace(" ", "")
    temp = temp.replace(",", "")

    temp = temp.split("</span>")[1]
    temp = temp.split("</nobr>")[0]
    temp = " ".join(temp.split())

    print("Found match in " + forumName + ": " + temp + " threads in total")
    return temp

# Function to scrape the last n thread IDs present within the forumID, and store it into the variable tid
# Input: the forum URL and count

def connect(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    temp = []
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    soup.prettify()

    # all threadIDs have the following id

    hrefs = soup.find_all("a", {"id": "jive-thread-0"})

    for href in hrefs:
        href = str(href)
        href = href.split('href="')[1].split("&")[0]
        # href of form threads.jspa?threadID=xxx
        temp.append(href)

    return temp


# Function to fetch all the messages inside each thread and store it into the final CSV file with tag as the name of the product
# Input: The thread URL, the target product name and the thread #

def fetch(url, fname, threadno):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, 'html.parser')
    soup.prettify()

    messages = []

    # all messages have the following subject class

    subs = soup.find("span", {"class": "jive-subject"})
    subs = subs.text.strip()

    msgs = soup.find_all("div", {"class": "jive-message-body"})

    for line in msgs:
        msg = line.text.strip()
        msg = msg.replace("\n", " ")
        messages.append(msg)

    with open('input/newdata.csv', 'a', encoding='utf-8', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter=',')
        writer.writerow([threadno, fname, subs + " " + messages[0]])

        for m in range(1, len(messages)):
            writer.writerow([threadno, fname, messages[m]])


# driver Function

def check():

    # global variables

    forumIDs = [30, 60, 24, 46, 58, 72, 86, 186]
    forumName = ["Amazon EC2", "Amazon RDS", "Amazon S3", "Amazon CloudFront", "Amazon VPC", "Amazon SNS", "Amazon Elastic Beanstalk", "Amazon Lambda"]
    threadLimit = []

    # fetch the updated numberOfThreads

    for i in range(0, 8):
        threadLimit.append(0)
        threadLimit[i] = updateNumberOfThreads(forumIDs[i], forumName[i])

    with open('input/newdata.csv', 'w', encoding='utf-8', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter=',')
        writer.writerow(["id", "label", "description"])


    df = pd.read_csv("input/NumberOfThreads.csv")

    difference = []

    for i in range(0, 8):
        print("Processing threads for", forumName[i])
        difference.append(int(threadLimit[i]) - int(df['NumberOfThreads'][i]))
        threads = []
        # limit = difference[i] # default value is 25
        limit = 3
        j = 0

        while j <= limit:
            try:
                url = "https://forums.aws.amazon.com/forum.jspa?forumID="+str(forumIDs[i])+"&start="+str(j)
                threads = threads + connect(url)
                j = j + 25
                # print("Fetched " + str(j) + " threads")
            except:
                print("Interrupt at thread #" + str(j))
                time.sleep(5)

        j = 0

        # print(threads)

        while j < limit:
              try:
                  # print("Processing thread #" + str(j))
                  fetch("https://forums.aws.amazon.com/" + threads[j], forumName[i], int(threadLimit[i])-j)
                  j = j + 1
              except:
                  print("Interrupt at thread #" + str(j))
                  time.sleep(5)

    # print(difference)

    with open('input/NumberOfThreads.csv', 'w', encoding='utf-8', newline='') as tsvfile:
        writer = csv.writer(tsvfile, delimiter=',')
        writer.writerow(["label", "NumberOfThreads"])

        for i in range(0, 8):
            writer.writerow([forumName[i], threadLimit[i]])
