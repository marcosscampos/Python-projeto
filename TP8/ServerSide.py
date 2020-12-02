import pickle
import socket
import logging as logger
from multiprocessing import Process

from Classes.functions.Rede import get_ip
from Classes.functions.Rede import hosts_detalhados
from Classes.functions.Processos import set_processos
from Classes.functions.Memoria import set_memoria
from Classes.functions.Disco import get_disk

logger.basicConfig(level=logger.INFO)

eventos = {
    'network': get_ip,
    'process': set_processos,
    'memory': set_memoria,
    'disk': get_disk,
    'hosts': hosts_detalhados
}


def socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    port = 7777

    server.bind((host, port))

    server.listen()

    logger.info(f'\tServidor {host} esperando conexão na porta: {port}')

    while True:
        (client, addr) = server.accept()
        logger.info(f'\tConectado na porta: {str(addr)}')

        event_name = client.recv(1024)
        name = str(event_name.decode('utf-8', 'ignore'))

        if name in eventos.keys():
            data = eventos[name]()
            client.send(pickle.dumps(data))

        if name in eventos.keys() != 'memory':
            client.close()


if __name__ == '__main__':
    logger.info(f'\tIniciando as Tarefas')
    try:
        socket_server()
    except Exception as ex:
        logger.error("\tNão foi possível iniciar o servidor.", ex)
    logger.info(f'\tTarefas finalizadas')
