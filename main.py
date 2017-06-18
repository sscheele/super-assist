""" An improved assistant piggybacking off of Google AVS"""
import threading
import re

class Channel:
	""" Channel allows communication/synchronization between threads"""
	def __init__(self):
		self.message = ""
		self.write_mutex = threading.Lock()
		self.read_mutex = threading.Lock()
		self.read_mutex.acquire()
	def write(self, msg):
		""" Write allows a message to be sent down the channel"""
		self.write_mutex.acquire()
		self.message = msg
		self.read_mutex.release()
	def read(self):
		""" read allows a message to be read from the channel """
		self.read_mutex.acquire()
		msg = self.message
		self.message = ""
		self.write_mutex.release()
		return msg

class ThreadOverseer:
	"""A class to watch all necessary threads"""
	def __init__(self):
		self.processes = {}
	def start_process(self, t_name, t_cls):
		"""start_process requires a name for the thread and a thread class to run"""
		self.processes[t_name] = t_cls
		self.processes[t_name].start()
	def kill_process(self, t_name):
		"""kill_process kills a process (all should reserve PKILL as a stop keyword)"""
		self.processes[t_name].chan.write("PKILL")
	def prune(self):
		"""prune removes finished threads from the dictionary"""
		self.processes = {a: b for a, b in self.processes.items() if b.is_alive()}
	def send_text(self, t_name, text):
		"""send_text sends text to a program"""
		self.processes[t_name].recv(text)
	def is_running(self, t_name):
		"""Check if an object with the name is running"""
		self.prune()
		return t_name in self.processes

class InputHandler:
	"""A class whose job is to watch for commands and route them as required"""
	def __init__(self):
		self.starters = {}
		self.commands = {}
	def add_starter(self, cls):
		"""add_starter matches a pattern to a command class"""
		self.starters[cls.pattern] = cls.thread_cls
		for tmp in cls.command_patterns:
			self.commands[tmp] = cls.name
	def handle_input(self, text):
		"""handle_input runs through the list of patterns trying to find a match for text"""


class Task:
	"""Task associates task names, command phrases, and thread classes"""
	def __init__(self, n, p, c, t):
		self.name = n
		self.pattern = p
		self.command_patterns = c
		self.thread_cls = t

i = 1
try:
	while True:
		_ = input()
		print(i)
		i += 1
except EOFError:
	pass
