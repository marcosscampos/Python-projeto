import psutil
import pygame
import socket

from Classes.Common import Cores
from Classes.Model import Rede, Arquivo

largura_tela = 800
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)
fontBold = pygame.font.SysFont('Segoe UI', 15, True)
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_rede = pygame.surface.Surface((largura_tela, altura_tela))
hosts = []


def mostrar_info_ip_rede():
    surface_rede.fill(Cores.preto)
    texto = 'Informações De Rede:'
    texto_font = font.render(texto, True, Cores.cinza)
    surface_rede.blit(texto_font, (20, 20))
    hosts = get_ip()
    aux = hosts
    gap = 85

    nome = '{:>5}'.format('INTERFACE')
    ip = '{:>30}'.format('IP')
    mascara = '{:>45}'.format("MÁSCARA")
    titulo_rede = nome + ip + mascara
    fonte_titulo_rede = fontBold.render(titulo_rede, True, Cores.cinza)
    surface_rede.blit(fonte_titulo_rede, (20, 65))

    for host in aux:
        ip = str(host.ip)
        if ip != '127.0.0.1':
            texto_interface = '{:>0}'.format(Arquivo.Arquivo.ajusta_nome_arquivo(host.interface))
            texto_ip = '{:>35}'.format(host.ip)
            texto_mascara = '{:>45}'.format(str(host.mascara))
            texto_compilado = texto_interface + texto_ip + texto_mascara
            texto_tela = font.render(texto_compilado, True, Cores.cinza)
            surface_rede.blit(texto_tela, (20, gap))
            gap += 25

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_rede.blit(instrucao, (150, 560))
    return surface_rede


def mostrar_ips(sistema):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == sistema:
                rede = Rede.Rede(interface, snic.address, snic.netmask)
                yield rede


def get_ip():
    return list(mostrar_ips(socket.AF_INET))