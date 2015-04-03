# HN-sum
A website that takes the best stories from [Hacker News](https://news.ycombinator.com/)
and provides a brief summary of their articles. The live site can be found here:
[www.hn-sum.info](http://www.hn-sum.info)

## Instillation
### Docker
![Docker Badge](/docs/docker-badge.png)

A docker container is available for use and can be found at
[nicholasrutherford / hn-sum](https://registry.hub.docker.com/u/nicholasrutherford/hn-sum/).

To run the container:

    sudo docker run -d -p 80:80 nicholasrutherford/hn-sum

Then to view the site, simply go to your servers ip-address. The container is
set to update the content every hour.

### Manual Instillation
First, clone the repository:

    git clone https://github.com/nicholasRutherford/HN-sum.git
    cd HN-sum

Then install the prerequists:

    pip install -r requirements.txt

Then you'll need to install the extra NLTK data files.

    python bin/nltkSetup.py

#### Updating the Website
To fetch new stories and provide the summary:

    python hnSummarized/updateWebsite.py

 Then you can view the updated website in `hnSummarized/website/index.html`

## Algorithm
The algorithm used to provide the text summaries and keywords is the TextRank
algorithm outlined in the paper
[TextRank : Bringing Order into Texts](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf) by
Rada Mihalcea and Paul Tarau.

## License
![AGPL V3 logo](/docs/agplv3.png)

This code is licensed under the AGPL V3 license.
