"""
Various small functions used in the rest of the program.
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
import sys
import os
import json

INFO_JSON = "./hnSummarized/info.json"
FAILED_JSON = "./hnSummarized/failed.json"


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


def loadFailed():
    """Load the failed.json file

    Returns:
        list - list of strings of story IDs that failed to summarize

    Raises:
        Exit - If unable to open the fileName passed in.
    """
    try:
        rawFile = open(FAILED_JSON, "r")
        failed = json.load(rawFile)
        rawFile.close()
        return failed
    except IOError:
        rawFile = open(FAILED_JSON, "w+")
        rawFile.write("[]")
        rawFile.close()
        return []


def saveFailed(failed):
    """Saves the failed.json file

    Args:
        failed - The current failed list to save

    Raises:
        Exit - If unable to open the file
    """
    try:
        rawFile = open(FAILED_JSON, "w+")
    except IOError:
        print "Error: Can't open the file ", FAILED_JSON
        sys.exit(1)

    json.dump(failed, rawFile)
    rawFile.close()


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
