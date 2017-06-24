"""Search for and download videos"""
from html.parser import HTMLParser
from urllib.parse import quote_plus
from urllib.request import urlopen
from re import compile
import string
import random
import pafy
import os
import subprocess
from time import sleep
from input_classes import Task, Expression


def rand_str(N):
    """ return a random string of length N """
    return ''.join([random.choice(string.ascii_uppercase + string.digits) for i in range(N)])


class YTParser(HTMLParser):
    """ YTParser parses YouTube search results """

    def __init__(self, t):
        super().__init__()
        self.data = ""
        self.target = t
        self.iterations = 0

    def handle_starttag(self, tag, attrs):
        """ return the first video link """
        if self.data != "" and self.iterations > self.target:
            return
        # try the first a tag with a title and a link to /watch?=...
        if tag == 'a':
            for attr_name, attr_val in attrs:
                if attr_name == "href" and attr_val.startswith("/watch?v="):
                    self.data = attr_val[9:]
                    self.iterations += 1


def search_yt(query, chan):
    """ Return the first youtube result for a link """
    print("Started")
    url = "https://www.youtube.com/results?search_query=" + quote_plus(query)
    i = 0
    vid_obj = None
    duration = 0
    while vid_obj is None:
        parser = YTParser(i)
        parser.feed(str(urlopen(url).read()))
        vid_id = parser.data
        print(vid_id)
        vid_obj = pafy.new(
            "http://www.youtube.com/watch?v=" + vid_id).getbestaudio()
    vid_file = vid_id + "." + vid_obj.extension
    print(vid_obj.download(quiet=True, filepath=vid_file))
    player = subprocess.Popen(
        ["avplay", vid_file, "-autoexit"], stdout=subprocess.PIPE)
    while player.poll() is None:
        if chan.is_full():
            tmp = chan.read()
            if tmp == "pause" or tmp == "play":
                p = subprocess.Popen(['xte'], stdin=PIPE)
                p.communicate(input="""p
                """)
        sleep(.07)
    os.remove(vid_file)
    print(chan.read())


YT_TASK = Task("youtube",
               [Expression(compile(r"search for (.*) on youtube"), ('query'))],
               [Expression(compile("pause"), ("command")),
                Expression(compile("play"), ("command"))
                ],
               search_yt)
