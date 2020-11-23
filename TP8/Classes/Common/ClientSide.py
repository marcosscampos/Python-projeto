import pickle
import socket
import sys


class Client:
    _instance = None

    def __init__(self):
        self._port = 9999
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
        except Exception as ex:
            print(str(ex))
            sys.exit(1)

        return pickle.loads(data)
