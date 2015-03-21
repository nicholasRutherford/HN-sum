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


def isGoodStory(story):
    """Determins if a story is 'good', aka greater than 100 votes
        or is about haskell

    Args:
        story (dict) - A dictionary reprenting an HN item query result

    Returns:
        bool. True if the story is 'good', false otherwise
    """
    if story["title"].lower().count('haskell') > 0:
        return True
    if story["score"] < 100:
        return False
    return True


def newOnly(storyIDs, info):
    """Takes all the stories and removes any which we've already downloaded

    Args:
        storyIDs ([int]) - A list of HN story IDs
        info (dict) - Dictionary of information on downloaded stories

    Returns:
        [int]. A list of HN story IDs for new stories only
    """
    newStories = []
    for sID in storyIDs:
        try:
            _ = info[str(sID)]
            print "Already have: ", sID
        except KeyError:
            newStories.append(sID)
    return newStories

def goodOnly(storyIDs):
    """Takes all the stories and filters out any story that isn't good

    Args:
        storyIDs ([int]) - A list of HN story IDs

    Returns:
        [dict]. A list of HN story dictionaries
    """

    goodStories = []
    for sID in storyIDs:
        r = requests.get(BASE_URL + "item/" + str(sID) + ".json")
        query = r.json()
        try:
            if isGoodStory(query):
                goodStories.append(query)
                print query["title"], query["score"]
        except KeyError:
            print "Error on ", str(sID)
    return goodStories

def getStories(info):
    """Get the story IDs corresponding to good articles only

    Args:
        info (dict) - Dictionary of information on downloaded stories

    Returns:
        [dict]. A list of HN story dictionaries
    """

    # Get top stories
    r = requests.get(BASE_URL + "topstories.json")
    storyIDs =  r.json()[:CUT_OFF]

    # Filter stories so only new, good stories are downloaded
    return goodOnly(newOnly(storyIDs, info))

def downloadStory(story, url):
    """Save the content linked to by a story into the HTML_DIR

    Args:
        story (dict) - HN story dictionary
        url (str) - The url linked by the story

    Raises:
        urllib2.HTTPError
        urllib2.URLError
    """
    # Download the link
    response = urllib2.urlopen(url)
    rawHtml = response.read()

    # File name
    name = str(story["id"]) + ".html"

    # Save the html file
    d = datetime.fromtimestamp(story["time"]).date().isoformat()
    path = HTML_DIR + d +"/"

    sumUtil.saveAndMakePath(path, name, rawHtml)


def updateInformation(story, url, info):
    """Update the information file with the new story

    Args:
        story (dict) - HN story dictionary
        url (str) - The url linked by the story
        info (dict) - Dictionary of information on downloaded stories

    """
    title = story["title"]
    comments = HN_BASE + str(story["id"])

    i = {'title': title,
            'comments': comments,
            'url': url}

    info[str(story["id"])] = i

def downloadStories():
    """Find the latest HN stories and download their linked content"""
    info = sumUtil.loadInfo()

    stories = getStories(info)

    print "downloading..."
    for story in stories:
        try:
            # If it is an internal link, preface it with base url
            if story["url"] == "":
                url = HN_BASE + str(story["id"])
            else:
                url = story["url"]

            downloadStory(story, url)
            updateInformation(story, url, info)
        except (urllib2.HTTPError, urllib2.URLError, ValueError):
            print "Error on : ", story["title"]

    sumUtil.saveInfo(info)

if __name__ == '__main__':
    downloadStories()
