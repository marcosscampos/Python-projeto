import psutil
import pygame

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Calibri', 25)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_cpu = pygame.surface.Surface((largura_tela, altura_tela/4))

def mostra_uso_cpu():
    porcentagem = psutil.cpu_percent(interval=0)
    largura = largura_tela - 2 * 20

    pygame.draw.rect(surface_cpu, Cores.azul_claro, (20, 50, largura, 70))
    tela.blit(surface_cpu, (0, 0))

    largura = largura * porcentagem / 100
    pygame.draw.rect(surface_cpu, Cores.azul, (20, 50, largura, 70))
    tela.blit(surface_cpu, (0, 0))

    text = font.render(f"Uso de CPU: {str(porcentagem)}%", 1, Cores.branco)
    tela.blit(text, (20, 15))