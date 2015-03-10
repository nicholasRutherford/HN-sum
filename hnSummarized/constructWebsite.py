"""
Author: Nicholas Rutherford
License: MIT
"""

import os
import json
import datetime
import sys

import websiteBlocks


INFO_JSON = "./hnSummarized/info.json"
SUM_DIR = "./hnSummarized/summaries/"
WEBSITE = "./hnSummarized/website/index.html"
STORIES_PER_ROW = 2

def loadInfo(fileName):
    """Load the info.json file

    Args:
        fileName (str): The path to info.json.

    Returns:
        dict.  A dictionary whose keys are story ID's and contents are:
                url - The link to the story
                comments - The link to the HN comment section
                title - The title of the story

    Raises:
        Exit - If unable to open the fileName passed in.
    """
    try:
        infoFile = open(fileName, "r")
    except IOError:
        print "Error: Can't open the info.json file"
        sys.exit(1)

    info = json.load(infoFile)
    infoFile.close()

    return info

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
            y, m , d = itemDate.split("-")
            dateOb = datetime.date(int(y), int(m), int(d))
        except ValueError:
            print "Warning: Invalid date format:", itemDate
            dateText = "------"
        else:
            dateText = dateOb.strftime("%B %d, %Y") # January 01, 2015

        return websiteBlocks.DATE.format(dateText)

def listDirectory(directory):
    """List all the items in a directory, sorted in reverse by name.

    Args:
        directory (str): Path to the directory to list

    Returns:
        [str]: List of directory contents

    Raises:
        Exit - If unable to open the directory passed in.
    """
    try:
        folderList = os.listdir(directory)
    except OSError:
        print "Error: Can't open the directory ", directory
        sys.exit(1)

    folderList.sort(reverse=True)
    return folderList

def loadText(path):
    """Return the text in a file.

    Args:
        path (str): The path to the file.

    Returns:
        str. The text of the file.

    Raises:
        Exit. Invalid path given.
    """
    try:
        rawFile = open(path, "r")
    except IOError:
        print "Error: Can't open the file ", path
        sys.exit(1)

    rawText = rawFile.read()
    rawFile.close()
    return rawText

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
    summaryText = loadText(path)
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
    if storyNum % STORIES_PER_ROW  == 0:
        storyText += websiteBlocks.ROW

    storyText += formatStory(downFile, folder, info)

    # End a row
    if (storyNum % STORIES_PER_ROW) == (STORIES_PER_ROW - 1):
        storyText += websiteBlocks.ROW_END

    return storyText

def saveFile(text, fileName):
    """Save text in the given file.

    Args:
        text (str): The text to save
        fileName (str): The file to save the text into

    Raises:
        IOError. If unable to open file.
    """

    ofile = open(fileName, "w+")
    ofile.write(text)
    ofile.close()


def constructWebsite():
    """Contructs a website from the summarized data

    Requirements:
        Summaries must be stored in the summaries folder, with a subfolder
        for separate dates.

    WEBSITE denotes where the file is saved
    """

    # Load saved HN api data
    info = loadInfo(INFO_JSON)

    webpage = ""
    webpage += websiteBlocks.HEADER

    storyNum = 0

    folderList = listDirectory(SUM_DIR)
    for folder in folderList:

        webpage += formatDate(folder)

        fileList = listDirectory(SUM_DIR + folder)
        for downFile in fileList:
            webpage += formatRows(downFile, folder, info, storyNum)
            storyNum += 1

    saveFile(webpage, WEBSITE)
