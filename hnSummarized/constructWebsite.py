"""
Constructs the website given the text summaries.
Copyright (C) 2015 Nicholas Rutherford

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import datetime
import sys
import os
import websiteBlocks
import sumUtil

SUM_DIR = "./hnSummarized/summaries/"
WEBSITE_DIR = "./hnSummarized/website/"
STORIES_PER_ROW = 2


def elementBlock(title, keywords, summary, article, comments):
    """Format given variables into the HTML code block for a story

    Args:
        title (str): The title of the story.
        keywords (str): The keywords associated with the story.
        summary (str): The story summary.
        article (str): The link to the actual story
        comments (str): The link to the HN comments page

    Returns:
        String. HTML code with the variables put into the correct locations
    """
    block = websiteBlocks.ELEMENT
    return block.format(title, keywords, summary, article, comments)


def formatDate(itemDate):
    """Format the date into the HTML code block for the date

    Args:
        itemDate (str): The date as a string in the form yyyy-mm-dd

    Returns:
        str. HTML code for the date
    """
    # Get the current date in the format yyyy-mm-dd
    today = datetime.datetime.now().date().isoformat()

    if itemDate == today:
        return websiteBlocks.DATE.format("Today")
    else:
        try:
            y, m, d = itemDate.split("-")
            dateOb = datetime.date(int(y), int(m), int(d))
        except ValueError:
            print "Warning: Invalid date format:", itemDate
            dateText = "------"
        else:
            dateText = dateOb.strftime("%B %d, %Y")  # January 01, 2015

        return websiteBlocks.DATE.format(dateText)


def loadHNData(info, fileID):
    """Load the data stored from the HN api

    Args:
        info (dict): Dictionay of HN data
        fileID (str): The unique ID of the story

    Returns:
        title (str): The title of the story
        article (str): The link to the actual story
        comments (str): The link to the HN comment section for this story

    Raises:
        Exit - Missing data for this file
    """
    try:
        title = info[fileID]["title"].encode("ascii", "ignore")
        article = info[fileID]["url"].encode("ascii", "ignore")
        comments = info[fileID]["comments"].encode("ascii", "ignore")
    except KeyError:
        print "Error: No info entry for ID: ", fileID
        sys.exit(1)
    return title, article, comments


def formatStory(downFile, folder, info):
    """Format the story data into the HTML code block for a story

    Args:
        downFile (str): The path to the summarized story
        folder (str): The folder of the story
        info (dict): Dictionary of HN data

    Returns:
        str. HTML code for the story

    Raises:
        Exit. If file can not be opened.
    """

    path = SUM_DIR + folder + "/" + downFile
    summaryText = sumUtil.loadFile(path)
    keywords, summary = summaryText.split("\n")

    # ID is the name of the file (excluding extension)
    fileID = downFile.split(".")[0]

    title, article, comments = loadHNData(info, fileID)

    return elementBlock(title, keywords, summary, article, comments)


def formatRows(downFile, folder, info, storyNum,):
    """Format the story into an element of the current row.

    Args:
        downFile (str): The path to the summarized story
        folder (str): The folder of the story
        info (dict): Dictionary of HN data
        storyNum (int): The current story number

    Returns:
        str. HTML code for this element of the row

    Raises:
        Exit. If file can not be opened.
    """

    storyText = ""

    # Start a new row
    if storyNum % STORIES_PER_ROW == 0:
        storyText += websiteBlocks.ROW

    storyText += formatStory(downFile, folder, info)

    # End a row
    if (storyNum % STORIES_PER_ROW) == (STORIES_PER_ROW - 1):
        storyText += websiteBlocks.ROW_END

    return storyText


def isToday(text):
    """Whether the given date is today

    Args:
        text (str): The date as a string in the form yyyy-mm-dd

    Returns:
        bool. True if the given date is today
    """
    return datetime.date.today().isoformat() == text


def isYesterday(text):
    """Whether the given date is yesterday

    Args:
        text (str): The date as a string in the form yyyy-mm-dd

    Returns:
        bool. True if the given date is yesterday
    """
    yest = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    return text == yest


def pagerIndex():
    """Format the next page button on the index page

    Returns:
        str. HTML code for the page buttons
    """
    twoDays = (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
    twoDays += ".html"
    return websiteBlocks.PAGER_INDEX.format(twoDays)


def pager(text):
    """Format the next, and previous buttons on the non-index pages

    Args:
        text (str): The date as a string in the form yyyy-mm-dd

    Returns:
        str. HTML code for the page button
    """
    year, month, day = text.split("-")
    thisDate = datetime.date(int(year), int(month), int(day))
    next = (thisDate - datetime.timedelta(days=1)).isoformat() + ".html"
    prev = (thisDate + datetime.timedelta(days=1)).isoformat() + ".html"
    today = datetime.date.today().isoformat() + ".html"
    yest = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    yest += ".html"

    if os.path.isfile(next):
        return websiteBlocks.PAGER.format(prev, next)
    else:
        if prev == today or prev == yest:
            return websiteBlocks.PAGER_END.format("index.html")
        else:
            return websiteBlocks.PAGER_END.format(prev)


def constructWebsite():
    """Contructs a website from the summarized data

    Requirements:
        Summaries must be stored in the summaries folder, with a subfolder
        for separate dates.

    WEBSITE denotes the directory where the website files are saved
    """

    # Load saved HN api data
    info = sumUtil.loadInfo()

    webpage = ""
    webpage += websiteBlocks.HEADER

    for folder in sumUtil.listDirectory(SUM_DIR):
        storyNum = 0

        webpage += formatDate(folder)

        fileList = sumUtil.listDirectory(SUM_DIR + folder)
        for downFile in fileList:
            webpage += formatRows(downFile, folder, info, storyNum)
            storyNum += 1

        # Close rows with imperfect number of stories
        if len(fileList) % STORIES_PER_ROW != 0:
            webpage += websiteBlocks.ROW_END

        # Paganation
        if isToday(folder):
            continue
        elif isYesterday(folder):
            webpage += pagerIndex()
            webpage += websiteBlocks.FOOTER
            sumUtil.saveFile(webpage, WEBSITE_DIR + "index.html")

            webpage = ""
            webpage += websiteBlocks.HEADER
            storyNum = 0
        else:
            webpage += pager(folder)
            webpage += websiteBlocks.FOOTER
            sumUtil.saveFile(webpage, WEBSITE_DIR + folder + ".html")

            webpage = ""
            webpage += websiteBlocks.HEADER
            storyNum = 0


if __name__ == '__main__':
    constructWebsite()
