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


def getStation(title):
    titleRe = compile(r"(\d+)\).+")
    pandora = subprocess.Popen(
        ["pianobar"], stdout=subprocess.PIPE,  shell=True, preexec_fn=os.setsid)
    while True:
        # remove ANSI sequence before and newline after
        line = pandora.stdout.readline().decode('utf-8')
        m = titleRe.match(line[6:-1])
        if title.lower() in line.lower() and m:
            return m.group(1)
        if line.startswith("[?]"):
            os.killpg(os.getpgid(pandora.pid), SIGTERM)
    return ""


def pandorify(args, chan):
    """ Return the first youtube result for a link """
    print("Started", args['station'])
    num_extractor = compile(r"(\d+)\).+")
    track_num = getStation(args['station'])
    if track_num == "":
        print("Bad search pattern")
        return
    with open(os.devnull, 'wb') as throw_away:
        pandora = subprocess.Popen(
            ["pianobar"], stdin=subprocess.PIPE, stdout=throw_away)
        pandora.stdin.write(bytes(track_num + "\n", "UTF-8"))
        pandora.stdin.flush()
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
            pandora.stdin.write(bytes(key, 'UTF-8'))
            pandora.stdin.flush()
            if tmp == "PKILL":
                return


PANDORA_TASK = Task("pandora",
                    [Expression(compile(r"^play (.+) radio on pandora$"), ('station',)),
                     Expression(compile(r"^play (.+) on pandora$"),
                                ('station',)),
                     ],
                    [Expression(compile("^pause$"), ("command",)),
                        Expression(compile("^play$"), ("command",)),
                        Expression(compile("^like$"), ("command",)),
                        Expression(compile("^thumbs up$"), ("command",)),
                        Expression(compile("^unlike$"), ("command",)),
                        Expression(compile("^thumbs down$"), ("command",)),
                        Expression(compile("^next$"), ("command",))
                     ],
                    pandorify)
