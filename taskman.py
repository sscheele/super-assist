""" Classes to help with task managment and input handling """
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
		self.starters = {}
		self.commands = {}
		self.overseer = ThreadOverseer()
	def add_starter(self, cls):
		"""add_starter matches a pattern to a command class"""
		for tmp in cls.starters:
			self.starters[tmp] = cls
		for tmp in cls.command_patterns:
			self.commands[tmp] = cls

	def handle_input(self, text):
		"""handle_input runs through the list of patterns trying to find a match for text"""
		for key, val in self.starters:
			match_data = key.pattern.match(text)
			if match_data:
				tmp = val.thread_cls(key.arg_names, match_data.groups())
				self.overseer.start_process(val.name, tmp)
				return
		for key, val in self.commands:
			match_data = key.pattern.match(text)
			if match_data:
				if self.overseer.is_blocked(val.name):
					print("Error: blocked channel")
					return
				self.overseer.send_text(val.name, text)

class Task:
	"""Task associates task names, starter phrases, command phrases, and thread classes
	phrases should be represented by Expressions"""
	def __init__(self, n, s, c, t):
		self.name = n
		self.starters = s
		self.command_patterns = c
		self.thread_cls = t
