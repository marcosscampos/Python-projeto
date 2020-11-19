import psutil
import pygame

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Calibri', 25)
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_disco = pygame.surface.Surface((largura_tela, altura_tela/4))

def mostrar_uso_disco():
    disco = psutil.disk_usage('.')
    largura = largura_tela - 2*20
    pygame.draw.rect(surface_disco, Cores.verde_claro, (20, 30, largura, 70))
    tela.blit(surface_disco, (0, 300))

    largura = largura*disco.percent/100
    pygame.draw.rect(surface_disco, Cores.verde, (20, 30, largura, 70))
    tela.blit(surface_disco, (0, 300))

    total = round(disco.total/(1024*1024*1024), 2)
    used = round(disco.used/(1024*1024*1024), 2)
    texto_barra = f"Uso de disco: (Total: {str(total)}GB - {str(disco.percent)}% - {str(used)}GB)"
    text = font.render(texto_barra, 1, Cores.branco)
    tela.blit(text, (20, 295))