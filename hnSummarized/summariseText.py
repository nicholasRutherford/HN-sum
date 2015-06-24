"""
Takes the raw text and runs the sentence and keyword extraction.
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
from sentenceSelection import selectSentences
from keywordExtraction import extractKeywords
import sumUtil
import os


TEXT_DIR = "./hnSummarized/text/"
SUM_DIR = "./hnSummarized/summaries/"
NUM_SENTENCES = 10
NUM_KEYWORDS = 4


def hasFailedBefore(downfile):
    """Checks if a file has failed before

    Args:
        downfile (str) - The current file to check

    Returns:
        Bool - Wether the file has failed to summarize previously
    """
    failed = sumUtil.loadFailed()
    return downfile in failed


def checkIn(downfile):
    """Mark a file as failing.

    Args:
        downfile (str) - The current file to check

    Notes:
        The file is marked as failed, then it is summarized. If the summary
        runs fine, then the file is removed from the failing list. If the
        summary runs into a segfault, then the file will remain marked
        as failed, and will not be tried again.
    """
    failed = sumUtil.loadFailed()
    failed.append(downfile)
    sumUtil.saveFailed(failed)


def checkOut(downfile):
    """Mark a file as completed succesfully.

    Args:
        downfile (str) - The current file to check
    """
    failed = sumUtil.loadFailed()
    failed.remove(downfile)
    sumUtil.saveFailed(failed)


def summariseAll():
    for folder in sumUtil.listDirectory(TEXT_DIR):
        for downFile in sumUtil.listDirectory(TEXT_DIR + folder):
            if not os.path.isfile(SUM_DIR + folder + "/" + downFile):
                print downFile
                if (not hasFailedBefore(downFile)):
                    checkIn(downFile)
                    path = TEXT_DIR + folder + "/" + downFile

                    rawText = sumUtil.loadFile(path)

                    # Summarise
                    summary = selectSentences(rawText, NUM_SENTENCES)

                    # Key Words
                    keyWordsList = extractKeywords(rawText, NUM_KEYWORDS)
                    keyWords = " | ".join(keyWordsList)

                    toSave = keyWords + "\n" + summary
                    sumUtil.saveAndMakePath(SUM_DIR + folder + "/",
                                            downFile, toSave)
                    checkOut(downFile)


if __name__ == "__main__":
    summariseAll()
