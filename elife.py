#!/usr/bin/env python2


'''
Created on 4 Aug 2016

@author: sun
'''

import urllib.request

def eLifeRequest():    
    url = 'https://elifesciences.org'
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
        
        articles = {}
        
        sections = soup.find_all('section')
        for section in sections:
            if 'home-article-listing-wrapper' in section['class']:
                divs = section.find_all('div')
                for div in divs:
                    if 'view-elife-latest-research' in div['class']:
                        articleSource = div
                
                contentDict = {}
                titleInfo = articleSource.find_all('h2')
                #print(titleInfo)
                for item in titleInfo:
                    articles[str(item.text)] = item.a.get('href')
                    
        return(articles)
                           
    except Exception as e:
        print(e)

    
    
def main():
    latest = eLifeLatest()
    print(latest)
    
if __name__ == '__main__':
    main()