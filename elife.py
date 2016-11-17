#!/usr/bin/env python2


'''
Created on 4 Aug 2016

@author: sun
'''

import urllib.request
from urllib.parse import urljoin
import datetime
import time
import re

url = 'https://elifesciences.org'

def eLifeRequest():    
    global url
    headers = {'UserAgent':'Mozilla/5.0'}
    rqst = urllib.request.Request(url, headers=headers)
    rsp = urllib.request.urlopen(rqst)
    return(rsp)

def eLifePageSource():
    pagesource = eLifeRequest().read
    return(pagesource)

def eLifeSoup():
    import bs4 as bs
    
    eLifeRqst = eLifeRequest()
    pagesource = eLifeRqst.read()
    soup = bs.BeautifulSoup(pagesource, 'lxml')
    return(soup)

def eLifeGetSubjects():
    soup = eLifeSoup()
    
    subjects = {} ## dictionary with {'title':'links'}
    sections = soup.find_all('section')
    for section in sections:
        if 'section-content' in section['class']:
            ols = section.find_all('ol')
            for ol in ols:
                if 'home-subject-listing__list' in ol['class']:
                    subjectSource = ol
    
    links = subjectSource.find_all('a')
    for link in links:
        subjects[str(link.text)] = link.get('href')
        
    return(subjects)

def eLifeGetCatagories():
    soup = eLifeSoup()
    
    catagories = {} ## dictionary with {'title':'links'}
    footer = soup.find_all('footer')[0]
    ols = footer.find_all('ol')
    for ol in ols:
        try:
            if 'site-footer__section_links' in ol['class']:
                catagorySource = ol
        
        except:
            pass

    links = catagorySource.find_all('a')
    for link in links:
        catagories[str(link.text)] = link.get('href')
         
    return(catagories)

    
def eLifeLatest():
    try:
        soup = eLifeSoup()
            
        articles = {} ## {'title':{title:title, authors: [authors], link: link, abstract: abstract, digest:digest}}
        
        articleSource = soup.find_all("div", { "class" : "home-article-listing__list-item" })
    #     print(articleSourceAll)
        for article in articleSource:

            # Title
            titleInfo = article.find_all('h2')
            title = titleInfo[0].text

            # Link
            link = titleInfo[0].a.get('href')
            link = urljoin(url, link)
    
            # Authors
            authorInfo = article.find_all('li')
            authors = [author.text for author in authorInfo]

            # Impact statement
            impactInfo = article.find_all('span')    
            impact = impactInfo[0].text

            # Update date
            Date = article.find("time").attrs['datetime']
            Date = time.strptime(Date, "%Y-%m-%d")

            # Catagory
            Catagory = article.find("a", {"class" : "article-teaser__category"}).text
            
            ## Subjects
            SubjectInfo = article.find_all("a", {"class" : "article-teaser__heading"})
            Subject = [sub.text for sub in SubjectInfo]
            
            ## Link to lens
            LinkInfo = article.find("div", {"class" : "article-teaser__lens_link"})
            lenslink = LinkInfo.a.get('href')

            articles[title] = {"title" : title,
                               "authors" : authors,
                               "link" : link,
                               "Date" : Date,
                               "Impact" : impact,
                               "Catagory" : Catagory,
                               "Subject" : Subject,
                               "Lens" : lenslink}

        return articles

    except Exception as e:
        print(e,"Error")

def test():
    pass

def main():
    latest = eLifeLatest()
    print(latest)
     # eLifeLatest()
    
if __name__ == '__main__':
    main()
