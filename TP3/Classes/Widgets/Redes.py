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
    surface_rede.fill(Cores.preto)
    texto = 'Informações De Rede:'
    texto_font = font.render(texto, 1, Cores.cinza)
    surface_rede.blit(texto_font, (20, 20))
    hosts = mostrar_ips()
    aux = hosts
    gap = 60

    for host in aux:
        ip = str(host[1])
        if ip != '127.0.0.1':
            texto = font.render(host[0] + ": " + host[1], True, Cores.cinza)

            surface_rede.blit(texto, (20, gap))
            gap += 25

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_rede.blit(instrucao, (65, 560))
    return surface_rede


def mostrar_ips():
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            yield interface, snic.address


def get_ip():
    return list(mostrar_ips())
