import socket
import psutil

from Classes.Model.Rede import Rede


def set_ip(sistema):
    for pacotes in psutil.net_io_counters(pernic=True).items():
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == sistema:
                    rede = Rede(interface, snic.address, snic.netmask, pacotes)
                    yield rede


def get_ip():
    return list(set_ip(socket.AF_INET))
