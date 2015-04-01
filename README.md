# HN-sum
A summarized version of Hacker News

## Instillation Instructions
Step one, install the prerequists

    $ pip install -r requirements.txt

Then you'll need to install the extra NLTK data files.

    $ python # Open the interactive python interpreter
    ...
    >>> import nltk
    >>> nltk.download()

This will open a GUI for downloading NLTK resources. You'll want to use this to install the following:

* punkt
* maxent_treebank_pos_tagger
* stopwords

## Updating the website

    $ python hnSummarized/updateWebsite.py

 Then you can view the updated website in `hnSummarized/website/index.html`
