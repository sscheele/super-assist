""" Classes to help with task managment and input handling """
import re
import subprocess
import time
from thread_classes import ThreadOverseer


def gen_dict(keys, vals):
    """ generate a dictionary from tuples of keys and vals """
    retVal = {}
    for i in range(len(keys)):
        if i > len(vals):
            retVal[keys[i]] = ""
            continue
        retVal[keys[i]] = vals[i]
    return retVal


class Expression:
    """ Expression represents a way of phrasing a command - it contains a regex and a
    parallel set of argument names which correspond to capturing groups within the regex"""

    def __init__(self, pat, args):
        self.pattern = pat
        self.arg_names = args


class InputHandler:
    """A class whose job is to watch for commands and route them as required"""

    def __init__(self):
        self.commands = []
        self.overseer = ThreadOverseer()
        self.text_regexes = [re.compile(
            r"\{'text': '(.*)'\}"), re.compile("\\{'text': \"(.*)\"\\}")]

    def add_class(self, cls):
        """add_class matches a set of patterns to a Task"""
        self.commands.append(cls)

    def handle_input(self, text):
        """handle_input runs through the list of patterns trying to find a match for text"""
        for tsk in self.commands:
            for expr in tsk.starters:
                match_test = expr.pattern.match(text)
                if match_test:
                    arg_dict = {}
                    if len(match_test.groups()) == 0:  # informationless command
                        arg_dict = {expr.arg_names[0]: text}
                    else:
                        arg_dict = gen_dict(
                            expr.arg_names, match_test.groups())
                    self.overseer.start_process(
                        tsk.name, tsk.thread_func, arg_dict)
                    return
            if not self.overseer.is_running(tsk.name):
                continue
            for expr in tsk.command_patterns:
                match_test = expr.pattern.match(text)
                if match_test:
                    print("Attempting to send command '", text, "' to", tsk.name)
                    if self.overseer.is_blocked(tsk.name):
                        print("Error: blocked channel")
                        return
                    arg_dict = {}
                    if len(match_test.groups()) == 0:  # informationless command
                        arg_dict = {expr.arg_names[0]: text}
                    else:
                        arg_dict = gen_dict(
                            expr.arg_names, match_test.groups())
                    self.overseer.send_args(tsk.name, arg_dict)
                    return

    def scan_input(self):
        """ scan_input reads input from the console (really a pipe in practice),
        writes it to the console, and tries to parse it """
        proc = subprocess.Popen(["ssh", "-tt", "pi@127.0.0.1"],
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        # give time to connect
        time.sleep(5)
        proc.stdin.write(
            b"/home/pi/Desktop/GAssist/env/bin/google-assistant-demo\n")
        proc.stdin.flush()
        while True:
            next_line = proc.stdout.readline()
            if next_line != '':
                # the real code does filtering here
                tmp = next_line.decode("utf-8")
                print(tmp)
                tmp = tmp.strip().lower()
                for test_re in self.text_regexes:
                    match_test = test_re.match(tmp)
                    if match_test:
                        self.handle_input(match_test.group(1).strip())
            else:
                time.sleep(.01)


class Task:
    """Task associates task names, starter phrases, command phrases, and thread classes
    phrases should be represented by Expressions"""

    def __init__(self, n, s, c, t):
        self.name = n
        self.starters = s
        self.command_patterns = c
        self.thread_func = t
