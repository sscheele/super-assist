"""Search for and download videos"""
from html.parser import HTMLParser
from urllib.parse import quote_plus
from urllib.request import urlopen


class YTParser(HTMLParser):
    """ YTParser parses YouTube search results """

    def __init__(self):
        super().__init__()
        self.data = ""

    def handle_starttag(self, tag, attrs):
        """ return the first video link """
        if self.data != "":
            return
        # try the first a tag with a title and a link to /watch?=...
        if tag == 'a':
            for attr_name, attr_val in attrs:
                if attr_name == "href" and attr_val.startswith("/watch?v="):
                    self.data = attr_val[9:]


def search_yt(query):
    """ Return the first youtube result for a link """
    url = "https://www.youtube.com/results?search_query=" + quote_plus(query)
    parser = YTParser()
    parser.feed(str(urlopen(url).read()))
    print(parser.data)


search_yt("hello, world")
