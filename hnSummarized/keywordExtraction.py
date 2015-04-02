"""
Selects the best N keywords from a block of text.
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
import networkx as nx
import nltk
from nltk.corpus import stopwords


def removeStop(wordList, stopList):
    """Remove stop words from the word list

    Args:
        wordList ([str]) - List of words
        stopList ([str]) - List of words not to include

    Returns:
        [str] - List of words with stop words removed
    """
    goodWords = []
    for word in wordList:
        if word not in stopList:
            goodWords.append(word)
    return goodWords


def filterTags(wordList):
    """Remove words from the list that aren't nouns or adjectives

    Args:
        wordList ([str]) - List of words

    Returns:
        [str] - List containing only nouns and adjectives
    """
    filteredWords = []
    tagWords = nltk.pos_tag(wordList)
    for word, tag in tagWords:
        if tag == "NN" or tag == "JJ":
            filteredWords.append(word)

    return filteredWords


def word_tokenize(text, stop_words):
    """Convert a block of text into a list of nouns and adjectives with
        stop words removed

    Args:
        text (str) - Block of text
        stop_words ([str]) - List of words to ignore

    Returns:
        [str] - List of only nouns and adjectives with
                            stop words removed
    """
    wordList = nltk.word_tokenize(text)
    wordList = removeStop(wordList, stop_words)
    wordList = filterTags(wordList)
    return wordList


def add_nodes(g, wordList):
    """Add each word as a node in the graph

    Args:
        g (nx.graph) - The graph
        wordList ([str]) - List of words to add to the graph
    """
    for w in wordList:
        g.add_node(w)


def add_edges(g, wordList, threshold):
    """Add edges to the nodes, each word is connected to the threshold
        number of words after it

    Args:
        g (nx.graph) - The graph
        wordList ([str]) - List of words to add
        threshold (int) - The number of words to connect

    We connect each word with the N words after it in the list. For example
    if we are looking at the first word in the list, and threshold is 3
    the following directed edges are added:
        1 -> 2
        1 -> 3
        1 -> 4
    """

    for i, w in enumerate(wordList):
        for j in xrange(1, threshold+1):
            try:
                g.add_edge(w, wordList[i+j])
            except IndexError:
                pass


def construct_graph(g, wordList, threshold):
    """Adds nodes and edges according to the textRank algorithm

    Args:
        g (nx.graph) - The graph
        wordList ([str]) - List of words to add
        threshold (int) - Number of nodes to connect at once
    """
    add_nodes(g, wordList)
    add_edges(g, wordList, threshold)


def extract(wordList, K, threshold):
    """Finds K keywords from the word list

    Args:
        wordList ([str]) - List of words
        K (int) - Number of keywords to extract
        threshold (int) - Number of nodes to connect at once

    Returns:
        [str] - List of K keywords
    """
    g = nx.DiGraph()
    construct_graph(g, wordList, threshold)

    # Compute values
    pairs = nx.pagerank(g, max_iter=10).items()
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    return [x[0] for x in pairs[:K]]


def extractKeywords(rawText, K=4, threshold=5):
    """Take a block of text and extract K keywords from it

    Args:
        rawText (str) - Block of raw text
        K (int) - Number of keywords to extract
        thershold (int) - Number of nodes to connect at once

    Returns:
        [str] - List of K keywords
    """
    stop_words = stopwords.words('english')
    wordList = word_tokenize(rawText, stop_words)
    return extract(wordList, K, threshold)
