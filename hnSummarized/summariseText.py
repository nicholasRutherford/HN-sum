from sentenceSelection import selectSentences
from keywordExtraction import extractKeywords
import sumUtil


TEXT_DIR = "./hnSummarized/text/"
SUM_DIR  = "./hnSummarized/summaries/"
NUM_SENTENCES = 10
NUM_KEYWORDS = 4

for folder in sumUtil.listDirectory(TEXT_DIR):
    for downFile in sumUtil.listDirectory(TEXT_DIR + folder):
        path = TEXT_DIR + folder + "/" + downFile

        rawText = sumUtil.loadFile(path)

        # Summarise
        summary = selectSentences(rawText, NUM_SENTENCES)

        # Key Words
        keyWordsList = extractKeywords(rawText, NUM_KEYWORDS)
        keyWords = " | ".join(keyWordsList)

        toSave = keyWords + "\n" + summary
        sumUtil.saveAndMakePath(SUM_DIR + folder + "/", downFile, toSave)
