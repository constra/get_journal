'''
Created on 4 Aug 2016

@author: sun
'''
import requests
from bs4 import BeautifulSoup

elife = "https://elifesciences.org"
url = "https://elifesciences.org/archive/2016/08"
r = requests.get(url) #hard copy of a url
soup = BeautifulSoup(r.content, "lxml")

Article_titles = soup.find_all("div", {"class": "ds-1col"})

for i in Article_titles:
    print "Title" *10
    print i.contents[1].text # the title
    print "Title" *10
    a_u = elife + i.contents[1].find("a").get("href") #link
    a_r = requests.get(a_u)
    a_s = BeautifulSoup(a_r.content, "lxml")
    
    abstract = a_s.find("div", {"id": "abstract"})
    print "Abstract" *10
    print abstract.contents[1].text # the abstract
    print "Abstract" *10
    
    try:
        e_digest = a_s.find("div", {"id": "digest"})
        print "Digest" * 10
        print e_digest.contents[1].text # the eLife digest
        print "Digest" * 10
    except:
        continue
        