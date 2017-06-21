"""Search for and download videos"""
from html.parser import HTMLParser
from urllib.parse import quote_plus
from urllib.request import urlopen
from re import compile
import string
import random
from os import system
import pafy
from input_classes import Task, Expression

def rand_str(N):
    """ return a random string of length N """
    return ''.join([random.choice(string.ascii_uppercase + string.digits) for i in range(N)])

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


def search_yt(query, chan):
    """ Return the first youtube result for a link """
    print("Started")
    url = "https://www.youtube.com/results?search_query=" + quote_plus(query)
    parser = YTParser()
    parser.feed(str(urlopen(url).read()))
    vid_id = parser.data
    vid_obj = pafy.new("http://www.youtube.com/watch?v=" + vid_id).getbestaudio()
    vid_file = vid_id+"."+vid_obj.extension
    print(vid_obj.download(quiet=True, filepath=vid_file))
    system("xdg-open " + vid_file)
    print("Done")
    print(chan.read())


YT_TASK = Task("youtube", [Expression(compile(r"search for (.*) on YouTube"), ('query'))], [], search_yt)
