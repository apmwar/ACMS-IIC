import urllib
from bs4 import BeautifulSoup
from http.cookiejar import CookieJar
import csv

tid = []
messages = []
subjects = []
forumIDs = []

def loadcsv():
    with open('ForumID.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            forumIDs.append(row)

def connect(url):
    req = urllib.request.Request(url)
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(req)
    raw_response = response.read().decode('utf8', errors='ignore')
    
    soup = BeautifulSoup(raw_response, 'html.parser').encode("utf-8")
    soup.prettify()

    hrefs = soup.find_all("a", {"id": "jive-thread-0"})

    for href in hrefs:
        href = str(href)
        href = href.split('href="')[1].split("&")[0]
        tid.append(href)
    return tid

def fetch(url, fname):
    
    req = urllib.request.Request(url)
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(req)
    raw_response = response.read().decode('utf8', errors='ignore')
    
    soup = BeautifulSoup(raw_response, 'html.parser').encode("utf-8")
    soup.prettify()
    
    subs = soup.find_all("span", {"class": "jive-subject"})
    
    for line in subs:
        subjects.append(line.text.strip())
    
    msgs = soup.find_all("div", {"class": "jive-message-body"})
    
    for line in msgs:
        msg = line.text.strip()
        messages.append(msg)
        
        with open(fname + '.tsv', 'w', encoding='utf-8') as tsvfile:
            writer = csv.writer(tsvfile, delimiter='\t')
            for i, j in zip(subjects, messages):
                writer.writerow([fname, i + "\n" + j])

# Driver code begins here #

loadcsv()

limit = 75 # limit is actually 100 threads
counter = 1
end = 243

while counter < 1:
    
    i = 0

    while i <= limit:
        url = "https://forums.aws.amazon.com/forum.jspa?"+forumIDs[counter][1]+"&start="+str(i)
        print(url)
        tid = connect(url)
        i = i + 25
    
    for thread in tid:
        fetch("https://forums.aws.amazon.com/" + thread, "")

    counter = counter + 1