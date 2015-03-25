"""
Author: Nicholas Rutherford
License: MIT
"""

from bs4 import BeautifulSoup
import magic
import codecs
import sumUtil


HTML_DIR = "./hnSummarized/html/"
TEXT_DIR = "./hnSummarized/text/"


#Needed for the ascii encoder
def replace_spc_error_handler(error):
    return (u' ' * (error.end-error.start), error.end)

def isHTML(path):
    """Determines whether the file at the given path is an HTML file

    Args:
        path (str) - The path to the file that you want to check

    Returns:
        bool. True if the file is an HTML file, false otherwise
    """
    fileDesc = magic.from_file(path)
    return fileDesc.split(",")[0] == "HTML document"

def parseHTML(rawHtml):
    """Parses an HTML string into just the raw text

    Args:
        rawHtml (str) - A block of raw HTML code to parse

    Returns:
        str. The text contained in the HTML code
    """
    soup = BeautifulSoup(rawHtml, 'html.parser')
    paragraphs = soup.find_all('p')

    rawText = ""
    for para in paragraphs:
        rawText += para.get_text() + " "
    rawText = rawText.replace("\n", " ")
    return rawText.encode("ascii", "replace_spc")

def parseAll():
    """Parse all the downloaded HTML files into plain text.

    Output is saved into the corresponding folders in the
    directory TEXT_DIR
    """
    codecs.register_error("replace_spc", replace_spc_error_handler)

    for folder in sumUtil.listDirectory(HTML_DIR):
        for downFile in sumUtil.listDirectory(HTML_DIR + folder):
            rawText = ""
            path = HTML_DIR + folder + "/" + downFile
            if isHTML(path):
                rawHtml = sumUtil.loadFile(path)
                rawText = parseHTML(rawHtml)

            path = TEXT_DIR + folder +"/"
            fName = downFile.split(".")[0] + ".txt"
            sumUtil.saveAndMakePath(path, fName, rawText)

if __name__ == '__main__':
    parseAll()
