"""
Author: Nicholas Rutherford
License: MIT
"""

import nltk
import networkx as nx
from nltk.corpus import stopwords

import re


def word_tokenize(s, stop_words):
    """Convert a sentence into a list of words, excluding stop words

    Args:
        s (str) - A sentence to split into words
        stop_words ([str]) - A list of words to ignore

    Returns:
        [str] - The words of the sentence, not including stop_words
    """
    quality_words = []
    base = nltk.word_tokenize(s)
    for word in base:
        if word not in stop_words:
            quality_words.append(word)
    return quality_words


def tokeniseSentences(rawText):
    """Convert a block of text into a list of sentences

    Args:
        rawText (str) - A block of text

    Returns:
        [str] - List of sentences
    """
    # Remove newlines, sometimes mess up sentence detector
    rawText = rawText.replace("\n", " ")

    # Load pre-learned sentence detector, and split into sentences
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_detector.tokenize(rawText)


def add_nodes(g, sentList):
    """Add sentence nodes to the graph

    Args:
        g (nx.graph)- The graph
        sentList ([str]) - List of sentences
    """
    for sentence in sentList:
        g.add_node(sentence)


def add_edges(g, sentList,stop_words):
    """Add weighted edges to the graph

    Args:
        g (nx.graph) - The graph
        sentList ([str]) - List of sentences
        stop_words ([str]) - List of words to ignore
    """
    # Word tokenize each sentence
    token_list = []
    for sent in sentList:
        token_list.append((sent, word_tokenize(sent, stop_words)))

    # Compute the edge weight for two sentences
    for i, pair1 in enumerate(token_list):
        for j, pair2 in enumerate(token_list):
            if i < j:
                words1 = pair1[1]
                words2 = pair2[1]
                wordCount = 0
                for word in words1:
                    if word in words2:
                        wordCount += 1
                w = wordCount / float((len(words1) + len(words2)))
                g.add_edge(pair1[0], pair2[0], weight=w)


def construct_graph(g, sentList, stop_words):
    """Add nodes and edges to the graph according to the textRank algorithm

    Args:
        g (nx.graph) - The graph
        sentList ([str]) - List of sentences
        stop_words ([str]) - List of words to ignore
    """
    add_nodes(g, sentList)
    add_edges(g, sentList, stop_words)


def text_rank(sentList, stop_words):
    """Performs the textRank algorithm to obtain 'importance' scores for
        each sentence.

    Args:
        sentList ([str]) - List of sentences
        stop_words ([str]) - List of words to ignore

    Returns:
        [("str", Float)] - List of sentence, score pairs sorted descending by
                                score value
    """
    g = nx.Graph()

    construct_graph(g, sentList, stop_words)
    scores = nx.pagerank(g).items()
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return scores


def summary_para(scores, sentList, K):
    """Constructs the summary text selecting the K best sentences and
            formatting them in cronological order

    Args:
        scores [("str", Float)] - List of sentence, score pairs sorted
                                    descending by score value
        sentList ([str]) - List of sentencses
        K (int) - The number of sentences that the summary should be

    Returns:
        str - The K-sentence summary
    """
    good_sent = [x[0] for x in scores[:K]]
    count_check = dict(zip(good_sent, [0 for x in good_sent]))

    # Return sentences above cutoff in the order they appeared in the text
    toReturn = ""

    skip = False  # Used to insert '[...]' when sentences are skipped
    for sentence in sentList:
        if sentence in good_sent:
            if count_check[sentence] > 0:
                continue
            if skip:
                toReturn += " [...] "
            else:
                toReturn += " "
            toReturn += sentence
            skip = False
        else:
            skip = True

    # Remove all excessive whitespace
    return re.sub(r'\s+', ' ', toReturn).strip()


def selectSentences(rawText, K):
    """Summarise text into K sentences using textRank

    Args:
        rawText (str) - Block of text to be summarized
        K (int) - Number of sentences that the summary should be

    Returns:
        str - The K-sentence summary
    """
    stop_words = stopwords.words('english')
    sentList = tokeniseSentences(rawText)
    scores = text_rank(sentList, stop_words)

    return summary_para(scores, sentList, K)
