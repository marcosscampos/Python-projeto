import pygame
import platform
import subprocess
import nmap
import os
import threading

from Classes.Common import Cores
from Classes.Model import Arquivo, Hosts, Portas
from Classes.Common.ClientSide import Client

client = Client.instance()
network = client.use('network')
hosts = client.use('hosts')

largura_tela = 800
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)
fontBold = pygame.font.SysFont('Segoe UI', 15, True)
pygame.display.init()

surface_rede = pygame.surface.Surface((largura_tela, altura_tela))
# hosts_validos = []


def mostrar_info_ip_rede():
    surface_rede.fill(Cores.preto)
    texto = 'Informações De Rede:'
    texto_font = font.render(texto, True, Cores.cinza)
    surface_rede.blit(texto_font, (20, 20))

    aux = network
    gap = 85

    mostra_info_hosts_rede()
    # t = threading.Thread(target=hosts)
    # t.start()
    # t.join()
    # if len(hosts) == 0:
    #     t = threading.Thread(target=hosts)
    #     t.start()
    #     t.join()

    nome = '{:>5}'.format('INTERFACE')
    ip = '{:>30}'.format('IP')
    mascara = '{:>43}'.format("MÁSCARA")
    pacote_enviado = '{:>28}'.format('PCT. ENVIADO')
    pacote_recebido = '{:>28}'.format('PCT. RECEBIDO')
    titulo_rede = nome + ip + mascara + pacote_enviado + pacote_recebido
    fonte_titulo_rede = fontBold.render(titulo_rede, True, Cores.cinza)
    surface_rede.blit(fonte_titulo_rede, (20, 65))

    for host in aux:
        ip = str(host.ip)
        if ip != '127.0.0.1' and ip[0:3] != '169' and ip[0:3] != '172'\
                and host.pacotes[1][0] != '0' and host.pacotes[1][1] != 0:
            texto_interface = '{:>0}'.format(Arquivo.Arquivo.ajusta_nome_arquivo(host.interface))
            texto_ip = '{:>38}'.format(host.ip)
            texto_mascara = '{:>40}'.format(str(host.mascara))
            texto_pacote_enviado = '{:>25}'.format(str(round(host.pacotes[1][0] / (1024 ** 2), 2))) + 'MB'  # Enviado
            texto_pacote_recebido = '{:>30}'.format(str(round(host.pacotes[1][1] / (1024 ** 2), 2))) + 'MB'  # Recebido
            texto_compilado = texto_interface + texto_ip + texto_mascara + texto_pacote_enviado + texto_pacote_recebido
            texto_tela = font.render(texto_compilado, True, Cores.cinza)
            surface_rede.blit(texto_tela, (20, gap))
            gap += 25

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_rede.blit(instrucao, (150, 560))

    return surface_rede


def mostra_info_hosts_rede():
    gap = 170

    for host_rede in hosts:

        if host_rede.nome == "":
            host_rede.nome = "Nome não identificado."

        texto = font.render('IP:' + host_rede.ip + ' - Nome: ' + host_rede.nome, True, Cores.cinza)
        surface_rede.blit(texto, (20, gap))
        gap += 15

        for porta in host_rede.portas:
            if porta.portas != "" and porta.estado != "":
                texto_porta_estado = f'Porta: {str(porta.portas)} - Estado: {porta.estado}'
                textos = font.render(texto_porta_estado, True, Cores.cinza)
                surface_rede.blit(textos, (20, gap))
                gap += 20
        gap += 15

#
# def retorna_codigo_ping(hostname):
#     plataforma = platform.system()
#
#     if plataforma == "Windows":
#         args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]
#
#     else:
#         args = ['ping', '-c', '1', '-W', '1', hostname]
#
#     ret_cod = subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))
#     return ret_cod
#
#
# def get_hosts_rede(base_ip):
#     return_codes = dict()
#     threads = []
#     for i in range(1, 255):
#         t = threading.Thread(target=get_hosts_validos, args=(return_codes, base_ip, i))
#         threads.append(t)
#
#     for i in threads:
#         i.start()
#
#     for i in threads:
#         i.join()
#     print(f"\nOs host válidos são: {hosts_validos}")
#     print('\nMapeando portas...')
#     return hosts_validos
#
#
# def get_hosts_validos(return_codes, ip_base, i):
#     return_codes[ip_base + '{0}'.format(i)] = retorna_codigo_ping(ip_base + '{0}'.format(i))
#     if i % 20 == 0:
#         print(".", end="")
#     if return_codes[ip_base + '{0}'.format(i)] == 0:
#         hosts_validos.append(ip_base + '{0}'.format(i))
#
#
# def buscar_hosts():
#     ip = ''
#
#     for i in network:
#         if i.ip != '127.0.0.1' and i.ip[0:3] != '169':
#             ip = i.ip
#     ips_validos = ip
#     ip_principal = ips_validos
#
#     ip_string = ip_principal
#
#     ip_lista = ip_string.split('.')
#     base_ip = ".".join(ip_lista[0:3]) + '.'
#     print("O teste sera feito com a base: ", base_ip)
#
#     hosts_localizados = get_hosts_rede(base_ip)
#     detalhes_hosts(hosts_localizados)
#
#
# def detalhes_hosts(host_validos):
#     nm = nmap.nmap.PortScanner()
#     for host in host_validos:
#         try:
#             nm.scan(host)
#
#             ip = Hosts.Hosts(host, nm[host].hostname())
#
#             print(nm[host].hostname())
#             for proto in nm[host].all_protocols():
#
#                 lport = nm[host][proto].keys()
#
#                 for port in lport:
#                     porta = Portas.Portas(port, nm[host][proto][port]['state'])
#                     ip.portas.append(porta)
#         except Exception as ex:
#             print(ex, 'Não foi possível escanear as portas.')
#
#         if len(ip.portas) > 0:
#             for porta in ip.portas:
#                 print(f"Mapeado! Porta: [{str(porta.portas)} - {str(porta.estado)}]")
#         hosts_detalhados.append(ip)
