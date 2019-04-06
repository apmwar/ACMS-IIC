import requests
from bs4 import BeautifulSoup
import csv


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
}
res = requests.get("https://forums.aws.amazon.com/rss.jspa", headers=headers)
res.raise_for_status()
    
soup = BeautifulSoup(res.text, 'html.parser')
soup.prettify()
    
names = soup.find_all("td", {"class": "jive-first"})
fids = soup.find_all("td", {"class": "jive-last"})

    
Names = []
    
for name in names:
    name = str(name)
    pos = name.find("Forum:")
    if(pos > 0):
        name = name.split("Forum:")[1].split("</td>")[0]
    else:
        name = name.split("Category:")[1].split("<")[0]
    name = name.strip()
    name = name.replace("&amp;", "&")
    Names.append(name)
    
ForumIDS = []

for fid in fids:
    fid = str(fid)
    fid = fid.split('rss/rssannounce.jspa?')[1].split('"')[0]
    ForumIDS.append(fid)
    
    
for (i, j) in zip(Names, ForumIDS):
    with open("ForumID.csv", 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([i, j])


