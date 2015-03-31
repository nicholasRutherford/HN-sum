from sentenceSelection import selectSentences
from keywordExtraction import extractKeywords
import sumUtil
import os


TEXT_DIR = "./hnSummarized/text/"
SUM_DIR = "./hnSummarized/summaries/"
NUM_SENTENCES = 10
NUM_KEYWORDS = 4


def summariseAll():
    for folder in sumUtil.listDirectory(TEXT_DIR):
        for downFile in sumUtil.listDirectory(TEXT_DIR + folder):
            if not os.path.isfile(SUM_DIR + folder + "/" + downFile):
                print downFile
                path = TEXT_DIR + folder + "/" + downFile

                rawText = sumUtil.loadFile(path)

                # Summarise
                summary = selectSentences(rawText, NUM_SENTENCES)

                # Key Words
                keyWordsList = extractKeywords(rawText, NUM_KEYWORDS)
                keyWords = " | ".join(keyWordsList)

                toSave = keyWords + "\n" + summary
                sumUtil.saveAndMakePath(SUM_DIR + folder + "/", downFile, toSave)

if __name__ == "__main__":
    summariseAll()
