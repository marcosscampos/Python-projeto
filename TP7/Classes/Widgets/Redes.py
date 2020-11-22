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
tela = pygame.display.set_mode((largura_tela, altura_tela))
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

    buscar_trafego()

    nome = '{:>5}'.format('INTERFACE')
    ip = '{:>30}'.format('IP')
    mascara = '{:>25}'.format("MÁSCARA")
    pacote_enviado = '{:>20}'.format('PCT. ENVIADO')
    pacote_recebido = '{:>25}'.format('PCT. RECEBIDO')
    titulo_rede = nome + ip + mascara + pacote_enviado + pacote_recebido
    fonte_titulo_rede = fontBold.render(titulo_rede, True, Cores.cinza)
    surface_rede.blit(fonte_titulo_rede, (20, 65))

    for host in aux:
        interface = host.interface
        print(host)
        trafego_interface = mostrar_trafego_por_interface(interface)

        ip = str(host.ip)
        if ip != '127.0.0.1' and ip[0:3] != '169' and ip[0:3] != '171' and ip[0:3] != '172':
            # pacote_recebido = round(trafego_interface / (1024 ** 2), 2)
            # pacote_enviado = round(trafego_interface / (1024 ** 2), 2)

            texto_interface = '{:>0}'.format(Arquivo.Arquivo.ajusta_nome_arquivo(host.interface))
            texto_ip = '{:>38}'.format(host.ip)
            texto_mascara = '{:>32}'.format(str(host.mascara))
            texto_pacote_enviado = '{:>30}'.format(str(pacote_recebido)) + 'MB'
            texto_pacote_recebido = '{:>30}'.format(str(pacote_enviado)) + 'MB'
            texto_compilado = texto_interface + texto_ip + texto_mascara + texto_pacote_enviado + texto_pacote_recebido
            texto_tela = font.render(texto_compilado, True, Cores.cinza)
            surface_rede.blit(texto_tela, (20, gap))
            gap += 25

    if len(hosts_detalhados) == 0:
        texto_atencao = fontBold.render('Verificando a rede, aguarde.', True, Cores.branco)
        surface_rede.blit(texto_atencao, (275, 270))
    #
    # if len(hosts_detalhados) == 0:
    #     t = threading.Thread(target=buscar_hosts())
    #     t.start()

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_rede.blit(instrucao, (150, 560))
    return surface_rede


def mostra_info_hosts_rede():
    buscar_hosts()
    gap = 250

    porta = '{:>5}'.format('PORTA')
    estado = '{:>30}'.format('ESTADO')
    titulo_portas = porta + estado
    title = fontBold.render(titulo_portas, True, Cores.cinza)
    surface_rede.blit(title, (20, 300))

    for host_rede in hosts_detalhados:

        texto = font.render(host_rede.ip + ' - Nome: ' + host_rede.nome, True, Cores.cinza)
        surface_rede.blit(texto, (20, gap))
        gap += 15

        for porta in host_rede.portas:
            texto_porta = '{:>5}'.format(str(porta.portas))
            texto_estado = '{:>30}'.format(porta.estado)
            texto_porta_estado = texto_porta + texto_estado
            textos = font.render(texto_porta_estado, True, Cores.cinza)
            surface_rede.blit(textos, (40, gap))
            gap += 15

        gap += 15


def mostrar_ips(sistema):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == sistema:
                rede = Rede.Rede(interface, snic.address, snic.netmask)
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
    ips_validos = '192.168.1.'
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


def buscar_trafego():
    status = psutil.net_io_counters(pernic=True)
    hosts_ = hosts
    interface = []

    for host in hosts_:
        traffic = status[host[0]]
        enviado = traffic[0]
        recebido = traffic[1]
        pct_enviado = traffic[2]
        pct_recebido = traffic[3]

        aux = host[0] + enviado + recebido + pct_enviado + pct_recebido
        interface.append(aux)
    trafego.append(interface)


def mostrar_trafego_por_interface(interface):
    trafego_coletado = trafego
    trafego_exibir = trafego_coletado[len(trafego_coletado) - 1]
    retorno = ''

    for traffic in trafego_exibir:
        if traffic.interface == interface:
            retorno = traffic
            break

    return retorno
