import pickle
import socket

from Classes.functions.Rede import get_ip
from Classes.functions.Processos import set_processos
from Classes.functions.Memoria import set_memoria

eventos = {
    'network': get_ip,
    'process': set_processos,
    'memory': set_memoria
}


def socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = 7777

    server.bind((host, port))

    server.listen()

    print(f'Servidor {host} esperando conexão na porta: {port}')

    while True:
        (client, addr) = server.accept()
        print(f'Conectado na porta: {str(addr)}')

        event_name = client.recv(1024)
        name = str(event_name.decode('utf-8'))

        if name in eventos.keys():
            data = eventos[name]()
            client.send(pickle.dumps(data))

        if name in eventos.keys() != 'memory':
            client.close()


if __name__ == '__main__':
    socket_server()
