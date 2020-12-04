import pickle
import socket
import sys
from time import sleep
import logging as logger

logger.basicConfig(level=logger.INFO)


class Client:
    _instance = None

    def __init__(self):
        self._port = 7777
        self._host = socket.gethostname()

    @staticmethod
    def instance():
        if not Client._instance:
            Client._instance = Client()
        return Client._instance

    def use(self, event):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client.connect((self._host, self._port))
            client.send(event.encode('utf-8'))
            data = client.recv(100000)
            client.close()
        except:
            logger.info('\tAguardando a conexão com o servidor...')
            sleep(5)
            return self.use(event)

        return pickle.loads(data)
