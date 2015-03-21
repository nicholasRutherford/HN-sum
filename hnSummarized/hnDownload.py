"""
Author: Nicholas Rutherford
License: MIT
"""

import requests

from datetime import datetime
import urllib2

import sumUtil


HTML_DIR = "./hnSummarized/html/"
BASE_URL = "https://hacker-news.firebaseio.com/v0/"
HN_BASE = "https://news.ycombinator.com/item?id="
CUT_OFF = 100


def isGoodStory(q):
    """Determins if a story is 'good'"""
    if q["title"].lower().count('haskell') > 0:
        return True
    if q["score"] < 100:
        return False
    return True


def getStories(info):

    # Get top stories
    r = requests.get(BASE_URL + "topstories.json")
    rawLinks =  r.json()[:CUT_OFF]

    links = []
    for link in rawLinks:
        try:
            _ = info[str(link)]
            print "Already have: ", link
        except KeyError:
            links.append(link)

    goodStories = []
    for link in links:
        r = requests.get(BASE_URL + "item/" + str(link) + ".json")
        query = r.json()
        try:
            if isGoodStory(query):
                goodStories.append(query)
                print query["title"], query["score"]
        except KeyError:
            print "Error on ", str(link)

    return goodStories

def downloadLink(story, url):
    # File name
    name = str(story["id"]) + ".html"

    # Download the link
    response = urllib2.urlopen(url)
    rawHtml = response.read()

    # Save the html file
    d = datetime.fromtimestamp(story["time"]).date().isoformat()
    path = HTML_DIR + d +"/"
    sumUtil.saveAndMakePath(path, name, rawHtml)


def updateInformation(story, url, info):
    title = story["title"]
    comments = HN_BASE + str(story["id"])

    i = {'title': title,
            'comments': comments,
            'url': url}
    info[str(story["id"])] = i

def download():
    info = sumUtil.loadInfo()

    stories = getStories(info)

    # Download the links for good stories
    print "downloading..."
    for link in stories:
        try:
            # If it is an internal link, preface it with base url
            if link["url"] == "":
                url = HN_BASE + str(link["id"])
            else:
                url = link["url"]

            downloadLink(link, url)
            updateInformation(link, url, info)
        except (urllib2.HTTPError, urllib2.URLError, ValueError):
            print "Error on : ", link["title"]

    # store info file
    sumUtil.saveInfo(info)

if __name__ == '__main__':
    download()
