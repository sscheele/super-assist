""" Helpful classes for thread stuff """
from threading import Thread, Lock


class Channel:
    """ Channel allows communication/synchronization between threads"""

    def __init__(self):
        self.message = ""
        self.write_mutex = Lock()
        self.read_mutex = Lock()
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

    def is_full(self):
        """ return true if we can't write to the channel because it hasn't been read from yet """
        return self.write_mutex.locked()

class ThreadChan:
    """ ThreadChan is a container class for a thread and the channel it uses """
    def __init__(self, t, c):
        self.thread = t
        self.chan = c

class ThreadOverseer:
    """A class to watch all necessary threads"""

    def __init__(self):
        self.processes = {}

    def start_process(self, t_name, t_func, cmd):
        """start_process requires a name for the thread and a thread class to run"""
        chan = Channel()
        self.processes[t_name] = ThreadChan(Thread(target=t_func, args=(cmd, chan)), chan)
        self.processes[t_name].thread.start()

    def kill_process(self, t_name):
        """kill_process kills a process (all should reserve PKILL as a stop keyword)"""
        self.processes[t_name].chan.write("PKILL")

    def prune(self):
        """prune removes finished threads from the dictionary"""
        self.processes = {a: b for a,
                          b in self.processes.items() if b.thread.is_alive()}

    def send_text(self, t_name, text):
        """send_text sends text to a program"""
        self.processes[t_name].chan.write(text)

    def is_running(self, t_name):
        """Check if an object with the name is running"""
        self.prune()
        return t_name in self.processes

    def is_blocked(self, t_name):
        """ return true if a process isn't accepting input, false otherwise """
        return self.processes[t_name].chan.is_full()
