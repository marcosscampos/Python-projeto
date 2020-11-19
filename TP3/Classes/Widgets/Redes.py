import psutil
import pygame

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_rede = pygame.surface.Surface((largura_tela, altura_tela))
hosts = []


def mostrar_info_ip_rede():
    hosts = mostrar_ips()
    aux = hosts
    espacos = 100
    for host in aux:
        ip = str(host[1])
        if ip != '127.0.0.1':
            texto = font.render(host[0] + ": " + host[1], 1, Cores.cinza)

            surface_rede.blit(texto, (15, espacos))
            espacos += 25
    return surface_rede


def mostrar_ips():
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            yield interface, snic.address


def get_ip():
    return list(mostrar_ips())
