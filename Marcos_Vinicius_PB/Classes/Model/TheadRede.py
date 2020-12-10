import threading

from Classes.functions.Rede import buscar_hosts


class ThreadRede(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        buscar_hosts()
