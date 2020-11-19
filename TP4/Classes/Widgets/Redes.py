import psutil
import pygame

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Verdana', 15)
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_rede = pygame.surface.Surface((largura_tela, altura_tela))


def mostrar_info_ip_rede():
    mostra_texto(surface_rede, 'IP da máquina(Wi-Fi): ', 'Wi-Fi', 55)
    mostra_texto(surface_rede, 'IP da máquina(Ethernet): ', 'Ethernet', 80)
    mostra_texto(surface_rede, 'Máscara: ', 'netmask', 105)
    tela.blit(surface_rede, (20, 200))

    return surface_rede


def mostra_texto(superficie, nome, chave, pos_y):
    ip_wifi = psutil.net_if_addrs()['Wi-Fi'][1].address
    ip_ethernet = psutil.net_if_addrs()['Ethernet'][1].address
    mascara_wifi = psutil.net_if_addrs()['Wi-Fi'][1].netmask
    mascara_ethernet = psutil.net_if_addrs()['Ethernet'][1].netmask
    text = font.render(nome, True, Cores.branco)
    superficie.blit(text, (20, pos_y))

    if chave == 'Wi-Fi':
        if ip_wifi[0:3] == '169':
            s = 'Não conectado.'
        else:
            s = ip_wifi
    elif chave == 'Ethernet':
        if ip_ethernet[0:3] == '169':
            s = 'Não conectado.'
        else:
            s = ip_ethernet
    elif chave == 'netmask':
        if ip_ethernet[0:3] == '169':
            s = mascara_wifi
        else:
            s = mascara_ethernet
    text = font.render(s, 1, Cores.cinza)
    superficie.blit(text, (220, pos_y))
