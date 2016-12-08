#!/usr/bin/env python3


"""
Created on 4 Aug 2016
This is a class to retrieve information from the journal eLife
The Elife class should provide the downstream natural language processing enough information

I try to programm in a way that it is easy to scale up
@author: sun
"""

import urllib.request
from urllib.parse import urljoin
# import datetime
import time
# import re


class ELife:

    def __init__(self):
        self.url = 'https://elifesciences.org'


    def request(self, path):
        self.path = path
        self.headers = {'UserAgent': 'Mozilla/5.0'}
        self.rqst = urllib.request.Request(self.path, headers=self.headers)
        self.rsp = urllib.request.urlopen(self.rqst)
        return(self.rsp)

    def page_source(self, path):
        self.pagesource = self.request(path).read
        return(self.pagesource)

    def build_soup(self, path):
        import bs4 as bs

        request = self.request(path)
        pagesource = request.read()
        soup = bs.BeautifulSoup(pagesource, 'lxml')
        return(soup)

    def eLifeGetSubjects(self):
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

    def eLifeGetCatagories(self):
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


    def eLifeLatest(self):
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
    latest = ELife()
    info = latest.build_soup()
    print(info)
    
if __name__ == '__main__':
    main()
