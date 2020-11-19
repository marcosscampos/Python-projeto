import psutil
import pygame

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Calibri', 25)
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface = pygame.surface.Surface((largura_tela, altura_tela / 3))


def mostrar_info_ip_rede():
    texto = f"IP da Máquina: {ethernet_ou_wifi()}"
    text = font.render(texto, 1, Cores.branco)
    tela.blit(text, (20, 430))
    ethernet_ou_wifi()


def ethernet_ou_wifi():
    ip_info = psutil.net_if_addrs()
    ip = "Não conectado."

    if ip_info['Ethernet'][1].address[0:3] == '169':
        ip = ip_info['Wi-Fi'][1].address
    elif ip_info['Wi-Fi'][1].address[0:3] == '169':
        ip = ip_info['Ethernet'][1].address
    else:
        texto = "Não conectado."
        text = font.render(texto, 1, Cores.branco)
        tela.blit(text, (20, 430))

    return ip
