import hnDownload
import htmlParse
import summariseText
import constructWebsite


def update():
    hnDownload.downloadStories()
    htmlParse.parseAll()
    summariseText.summariseAll()
    constructWebsite.constructWebsite()

if __name__ == "__main__":
    update()
