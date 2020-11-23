import pickle
import socket

from Classes.Widgets.Arquivo import listar_arquivos
# from Classes.Widgets.Redes import buscar_hosts

eventos = {
    'archive': listar_arquivos
}


def servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 9999

    server.bind((host, port))

    server.listen()

    print('Server name', host, 'esperando conexão na porta', port)

    while True:
        (client, addr) = server.accept()
        print('Conectado a:', str(addr))

        event_name = client.recv(1024)
        name = str(event_name.decode('utf-8'))

        if name in eventos.keys():
            data = eventos[name]()
            client.send(pickle.dumps(data))

        client.close()


if __name__ == '__main__':
    servidor()