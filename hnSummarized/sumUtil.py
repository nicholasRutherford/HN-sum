import sys
import os
import json

INFO_JSON = "./hnSummarized/info.json"


def loadFile(path):
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


def loadInfo():
    """Load the info.json file

    Returns:
        dict.  A dictionary whose keys are story ID's and contents are:
                url - The link to the story
                comments - The link to the HN comment section
                title - The title of the story

    Raises:
        Exit - If unable to open the fileName passed in.
    """
    try:
        rawFile = open(INFO_JSON, "r")
        info = json.load(rawFile)
        rawFile.close()
        return info
    except IOError:
        rawFile = open(INFO_JSON, "w+")
        rawFile.write("{}")
        rawFile.close()
        return {}


def saveInfo(info):
    """Saves the info.json file

    Args:
        info - The current info dictionary to save

    Raises:
        Exit - If unable to open the file
    """
    try:
        rawFile = open(INFO_JSON, "w+")
    except IOError:
        print "Error: Can't open the file ", INFO_JSON
        sys.exit(1)

    json.dump(info, rawFile)
    rawFile.close()


def saveFile(text, path):
    """Save text in the given file.

    Args:
        text (str): The text to save
        path (str): The path to the file to save the text into

    Raises:
        IOError. If unable to open file.
    """
    try:
        ofile = open(path, "w+")
    except IOError:
        print "Error: Can't open the file ", path
        sys.exit(1)

    ofile.write(text)
    ofile.close()


def saveAndMakePath(folderPath, fileName, text):
    """Save the text into a file on the given path, creating parent
        folders as needed

    Args:
        folderPath (str) - The path to folder where the file will be saved
        fileName (str) - Name for the saved file
        text (str) - The text to save

    Raises:
        IOError. If unable to open file.
    """
    try:
        os.makedirs(folderPath)
    except OSError:
        if not os.path.isdir(folderPath):
            print "Error on making folder: ", folderPath
    saveFile(text, folderPath + fileName)


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
