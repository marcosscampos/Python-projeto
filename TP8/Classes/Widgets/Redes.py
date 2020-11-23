import psutil
import pygame
import socket
import platform
import subprocess
import nmap
import os
import threading

from Classes.Common import Cores
from Classes.Model import Rede, Arquivo, Hosts, Portas

largura_tela = 800
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)
fontBold = pygame.font.SysFont('Segoe UI', 15, True)
pygame.display.init()

surface_rede = pygame.surface.Surface((largura_tela, altura_tela))
hosts = []
hosts_detalhados = []
trafego = []


def mostrar_info_ip_rede():
    surface_rede.fill(Cores.preto)
    texto = 'Informações De Rede:'
    texto_font = font.render(texto, True, Cores.cinza)
    surface_rede.blit(texto_font, (20, 20))
    hosts = get_ip()
    aux = hosts
    gap = 85

    mostra_info_hosts_rede()
    if len(hosts_detalhados) == 0:
        t = threading.Thread(target=buscar_hosts())
        t.start()

    nome = '{:>5}'.format('INTERFACE')
    ip = '{:>30}'.format('IP')
    mascara = '{:>43}'.format("MÁSCARA")
    pacote_enviado = '{:>28}'.format('PCT. ENVIADO')
    pacote_recebido = '{:>30}'.format('PCT. RECEBIDO')
    titulo_rede = nome + ip + mascara + pacote_enviado + pacote_recebido
    fonte_titulo_rede = fontBold.render(titulo_rede, True, Cores.cinza)
    surface_rede.blit(fonte_titulo_rede, (20, 65))

    for host in aux:
        ip = str(host.ip)
        if ip != '127.0.0.1' and ip[0:3] != '169' and host.pacotes[1][0] != '0' and host.pacotes[1][1] != 0:
            texto_interface = '{:>0}'.format(Arquivo.Arquivo.ajusta_nome_arquivo(host.interface))
            texto_ip = '{:>38}'.format(host.ip)
            texto_mascara = '{:>40}'.format(str(host.mascara))
            texto_pacote_enviado = '{:>25}'.format(host.pacotes[1][0]) + 'MB'  # Enviado
            texto_pacote_recebido = '{:>30}'.format(host.pacotes[1][1]) + 'MB'  # Recebido
            texto_compilado = texto_interface + texto_ip + texto_mascara + texto_pacote_enviado + texto_pacote_recebido
            texto_tela = font.render(texto_compilado, True, Cores.cinza)
            surface_rede.blit(texto_tela, (20, gap))
            gap += 25

    if len(hosts_detalhados) == 0:
        texto_atencao = fontBold.render('Escaneando a rede, aguarde...', True, Cores.branco)
        surface_rede.blit(texto_atencao, (275, 270))

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_rede.blit(instrucao, (150, 560))

    return surface_rede


def mostra_info_hosts_rede():
    gap = 250

    for host_rede in hosts_detalhados:

        if host_rede.nome == "":
            host_rede.nome = "Nome não identificado."

        texto = font.render('IP:' + host_rede.ip + ' - Nome: ' + host_rede.nome, True, Cores.cinza)
        surface_rede.blit(texto, (20, gap))
        gap += 15

        for porta in host_rede.portas:
            texto_porta_estado = f'Porta: {str(porta.portas)} - Estado: {porta.estado}'
            textos = font.render(texto_porta_estado, True, Cores.cinza)
            surface_rede.blit(textos, (20, gap))
            gap += 20
        gap += 15


def mostrar_ips(sistema):
    for pacotes in psutil.net_io_counters(pernic=True).items():
        for interface, snics in psutil.net_if_addrs().items():
            for snic in snics:
                if snic.family == sistema:
                    rede = Rede.Rede(interface, snic.address, snic.netmask, pacotes)
                    yield rede


def get_ip():
    return list(mostrar_ips(socket.AF_INET))


def retorna_codigo_ping(hostname):
    plataforma = platform.system()
    args = []
    if plataforma == "Windows":
        args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]

    else:
        args = ['ping', '-c', '1', '-W', '1', hostname]

    ret_cod = subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
    return ret_cod


def get_hosts_rede(ip_base):
    hosts_validos = []
    return_codes = dict()
    for i in range(1, 255):

        return_codes[ip_base + '{0}'.format(i)] = retorna_codigo_ping(ip_base + '{0}'.format(i))
        if i % 20 == 0:
            print(".", end="")

        if return_codes[ip_base + '{0}'.format(i)] == 0:
            hosts_validos.append(ip_base + '{0}'.format(i))

    return hosts_validos


def buscar_hosts():
    ip = ''
    for i in get_ip():
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


def detalhes_hosts(host_validos):
    nm = nmap.nmap.PortScanner()
    for host in host_validos:
        try:
            nm.scan(host)

            ip = Hosts.Hosts(host, nm[host].hostname())

            print(nm[host].hostname())
            for proto in nm[host].all_protocols():

                lport = nm[host][proto].keys()

                for port in lport:
                    porta = Portas.Portas(port, nm[host][proto][port]['state'])
                    ip.portas.append(porta)
        except:
            pass

        hosts_detalhados.append(ip)
