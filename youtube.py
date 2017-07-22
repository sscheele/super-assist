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
import threading
from signal import SIGTERM
from input_classes import Task, Expression


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


def playAndDelete(player, filename, chan):
    """ play a file, then delete it """
    player.wait()
    os.remove(filename)
    chan.write("PKILL")


def search_yt(args, chan):
    """ Return the first youtube result for a link """
    print("Started", args['query'])
    url = "https://www.youtube.com/results?search_query=" + quote_plus(args['query'])
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
    with open(os.devnull, 'wb') as throw_away:
        player = subprocess.Popen(
            ["avplay", vid_file, "-autoexit"], stdout=throw_away, stderr=throw_away, preexec_fn=os.setsid)
        thrd = threading.Thread(target=playAndDelete, args=(player, vid_file, chan))
        thrd.start()
    while True:
        tmp = chan.read()["command"]
        if tmp == "pause" or tmp == "play":
            p = subprocess.Popen(['xte'], stdin=subprocess.PIPE)
            p.stdin.write(bytes("key space\n", 'UTF-8'))
            p.stdin.flush()
        elif tmp == "PKILL":
            os.killpg(os.getpgid(player.pid), SIGTERM) # this should also trigger a cleanup from playAndDelete
            return


YT_TASK = Task("youtube",
               [Expression(compile(r"search for (.+) on youtube"), ('query',)),
                Expression(compile(r"search youtube for (.+)"), ('query',)),
                Expression(compile(r"play (.+) on youtube"), ('query',)),
                ],
               [Expression(compile("pause"), ("command",)),
                Expression(compile("play"), ("command",))
                ],
               search_yt)
