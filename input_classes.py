""" Classes to help with task managment and input handling """
import re
from thread_classes import ThreadOverseer


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
        self.text_regex = re.compile(r"\{'text': '(.*)'\}")

    def add_class(self, cls):
        """add_class matches a set of patterns to a Task"""
        self.commands.append(cls)

    def handle_input(self, text):
        """handle_input runs through the list of patterns trying to find a match for text"""
        for tsk in self.commands:
            for expr in tsk.starters:
                if expr.pattern.match(text):
                    self.overseer.start_process(tsk.name, tsk.thread_func, text)
                    return
            if not self.overseer.is_running(tsk.name):
                continue
            for expr in tsk.command_patterns:
                if expr.pattern.match(text):
                    if self.overseer.is_blocked(tsk.name):
                        print("Error: blocked channel")
                    else:
                        self.overseer.send_text(tsk.name, text)
                    return

    def scan_input(self):
        """ scan_input reads input from the console (really a pipe in practice),
        writes it to the console, and tries to parse it """
        try:
            while True:
                tmp = input()
                print(tmp)
                match_test = self.text_regex.match(tmp)
                if match_test:
                    self.handle_input(match_test.group(1))
        except EOFError:
            pass


class Task:
    """Task associates task names, starter phrases, command phrases, and thread classes
    phrases should be represented by Expressions"""

    def __init__(self, n, s, c, t):
        self.name = n
        self.starters = s
        self.command_patterns = c
        self.thread_func = t
