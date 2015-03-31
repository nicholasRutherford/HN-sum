import hnDownload
import htmlParse
import summariseText
import constructWebsite


def update():
    print "Starting HN API..."
    hnDownload.downloadStories()
    print "Parsing..."
    htmlParse.parseAll()
    print "Summarizing..."
    summariseText.summariseAll()
    print "Constructing Website..."
    constructWebsite.constructWebsite()

if __name__ == "__main__":
    update()
