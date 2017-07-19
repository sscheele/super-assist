"""Search for and download videos"""
from re import compile
import string
import random
import os
import subprocess
from time import sleep
import threading
from signal import SIGTERM
from input_classes import Task, Expression


def getPlayList():
    titleRe = compile(r"\s+0\)\s+.+")
    pandora = subprocess.Popen(
        ["pianobar"], stdout=subprocess.PIPE,  shell=True, preexec_fn=os.setsid)
    while True:
        line = pandora.stdout.readline()
        if titleRe.match(line):
            yield line.strip()
        elif line.startswith("[?]"):
            os.killpg(os.getpgid(pandora.pid), SIGTERM)


def pandorify(args, chan):
    """ Return the first youtube result for a link """
    print("Started", args['query'])
    num_extractor = compile(r"(\d+)\).+")
    track_num = -1
    for title in getPlayList():
        if args['station'] in title:
            track_num = num_extractor.match(title).group(1)
    pandora = subprocess.Popen(
        ["pianobar"], stdout=subprocess.PIPE,  shell=True, preexec_fn=os.setsid)
    command_dict = {
        "pause": "p",
        "play": "p",
        "like": "+",
        "thumbs up": "+",
        "unlike": "-",
        "thumbs down": "-",
        "next": "n",
        "PKILL": "q"
    }
    while True:
        tmp = chan.read()["command"]
        key = command_dict[tmp]
        p = subprocess.Popen(['xte'], stdin=subprocess.PIPE,
                             shell=True, preexec_fn=os.setsid)
        p.stdin.write(bytes("key " + key + "\n", 'UTF-8'))
        p.stdin.flush()
        os.killpg(os.getpgid(p.pid), SIGTERM)
        if tmp == "PKILL":
            return

PANDORA_TASK = Task("youtube",
               [Expression(compile(r"play (.+) radio on pandora"), ('station',)),
                Expression(compile(r"play (.+) on pandora"), ('station',)),
                ],
               [Expression(compile("pause"), ("command",)),
                Expression(compile("play"), ("command",)),
                Expression(compile("like"), ("command",)),
                Expression(compile("thumbs up"), ("command",)),
                Expression(compile("unlike"), ("command",)),
                Expression(compile("thumbs down"), ("command",)),
                Expression(compile("next"), ("command",))
                ],
               pandorify)
