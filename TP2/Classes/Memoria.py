import psutil
import pygame

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Calibri', 25)
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_memoria = pygame.surface.Surface((largura_tela, altura_tela))


def mostra_uso_memoria():
    memoria = psutil.virtual_memory()
    largura = largura_tela - 2 * 20

    pygame.draw.rect(surface_memoria, Cores.roxo_claro, (20, 40, largura, 70))
    tela.blit(surface_memoria, (0, 150))

    total = round(memoria.total / (1024 * 1024 * 1024), 2)
    used = round(memoria.used / (1024 * 1024 * 1024), 2)

    largura = largura * memoria.percent / 100
    pygame.draw.rect(surface_memoria, Cores.roxo, (20, 40, largura, 70))
    tela.blit(surface_memoria, (0, 150))

    texto_barra = f"Uso de memória (Total: {str(total)}GB - {str(memoria.percent)}% - {str(used)}GB):"
    text = font.render(texto_barra, 1, Cores.branco)
    tela.blit(text, (20, 150))


