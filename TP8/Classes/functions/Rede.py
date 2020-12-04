import socket
import psutil
import nmap
import subprocess
import platform
import threading
import os

from Classes.Model.Rede import Rede
from Classes.Model.Hosts import Hosts
from Classes.Model.Portas import Portas

hosts_detalhados = []
hosts_validos = []


def set_ip(sistema):
    for pacotes in psutil.net_io_counters(pernic=True).items():
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == sistema:
                    rede = Rede(interface, snic.address, snic.netmask, pacotes)
                    yield rede


def get_ip():
    return list(set_ip(socket.AF_INET))


def retorna_codigo_ping(hostname):
    plataforma = platform.system()

    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]

    ret_cod = subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    return ret_cod


def get_hosts_rede(base_ip):
    return_codes = dict()
    threads = []
    for i in range(1, 255):
        t = threading.Thread(target=get_hosts_validos, args=(return_codes, base_ip, i))
        threads.append(t)

    for i in threads:
        i.start()

    for i in threads:
        i.join()
    print(f"\nOs host válidos são: {hosts_validos}")
    print('\nMapeando portas...')
    return hosts_validos


def get_hosts_validos(return_codes, ip_base, i):
    return_codes[ip_base + '{0}'.format(i)] = retorna_codigo_ping(ip_base + '{0}'.format(i))
    if i % 20 == 0:
        print(".", end="")
    if return_codes[ip_base + '{0}'.format(i)] == 0:
        hosts_validos.append(ip_base + '{0}'.format(i))


def buscar_hosts():
    hosts = get_ip()
    ip = ''

    for i in hosts:
        if i.ip != '127.0.0.1' and i.ip[0:3] != '169':
            ip = i.ip
    ips_validos = ip
    ip_principal = ips_validos

    ip_string = ip_principal

    ip_lista = ip_string.split('.')
    base_ip = ".".join(ip_lista[0:3]) + '.'
    print("O teste sera feito com a base: ", base_ip)

    hosts_localizados = get_hosts_rede(base_ip)
    detalhes_hosts(hosts_localizados)

    return hosts_detalhados


def detalhes_hosts(host_validos):
    nm = nmap.nmap.PortScanner()
    for host in host_validos:
        try:
            nm.scan(host)

            ip = Hosts(host, nm[host].hostname())

            if nm[host].hostname() != '':
                print(f'Nome: {nm[host].hostname()}')
            else:
                print('Nome não identificado.')

            for proto in nm[host].all_protocols():

                lport = nm[host][proto].keys()

                for port in lport:
                    porta = Portas(port, nm[host][proto][port]['state'])
                    ip.portas.append(porta)

            if len(ip.portas) > 0:
                for porta in ip.portas:
                    print(f"Mapeado! Porta: [{str(porta.portas)} - {str(porta.estado)}]")
            hosts_detalhados.append(ip)

        except Exception as ex:
            print(ex, 'Não foi possível escanear as portas.')

