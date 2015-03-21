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


def replace_spc_error_handler(error):
    return (u' ' * (error.end-error.start), error.end)

def isHTML(path):
    fileDesc = magic.from_file(path)
    return fileDesc.split(",")[0] == "HTML document"

def parseAll():
    codecs.register_error("replace_spc", replace_spc_error_handler)

    for folder in sumUtil.listDirectory(HTML_DIR):
        for downFile in sumUtil.listDirectory(HTML_DIR + folder):
            rawText = ""
            path = HTML_DIR + folder + "/" + downFile
            if isHTML(path):
                rawHtml = sumUtil.loadFile()
                soup = BeautifulSoup(rawHtml, 'html.parser')
                paragraphs = soup.find_all('p')

                for para in paragraphs:
                    rawText += para.get_text() + " "
                rawText = rawText.replace("\n", " ")
                rawText = rawText.encode("ascii", "replace_spc")

            path = TEXT_DIR + folder +"/"
            fName = downFile.split(".")[0] + ".txt"
            sumUtil.saveAndMakePath(path, fName, rawText)

if __name__ == '__main__':
    parseAll()
