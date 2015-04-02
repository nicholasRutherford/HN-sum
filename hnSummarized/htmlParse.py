"""
Parses an HTML page into plain text.
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

from bs4 import BeautifulSoup
import magic
import codecs
import sumUtil


HTML_DIR = "./hnSummarized/html/"
TEXT_DIR = "./hnSummarized/text/"


# Needed for the ascii encoder
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

            path = TEXT_DIR + folder + "/"
            fName = downFile.split(".")[0] + ".txt"
            sumUtil.saveAndMakePath(path, fName, rawText)

if __name__ == '__main__':
    parseAll()
