import psutil
import pygame

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_disco = pygame.surface.Surface((largura_tela, altura_tela))


def mostrar_uso_disco():
    largura = largura_tela - 2 * 20
    pygame.draw.rect(surface_disco, Cores.verde_claro, (20, 140, largura, 50))
    tela.blit(surface_disco, (0, 300))

    largura = largura * psutil.disk_usage('.').percent / 100
    pygame.draw.rect(surface_disco, Cores.verde, (20, 140, largura, 50))
    tela.blit(surface_disco, (0, 300))

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_disco.blit(instrucao, (65, 560))

    mostrar_texto(surface_disco, 'Espaço total: ', 'total', 55)
    mostrar_texto(surface_disco, 'Espaço usado: ', 'used', 80)
    mostrar_texto(surface_disco, 'Espaço livre: ', 'free', 105)
    tela.blit(surface_disco, (0, 150))

    return surface_disco


def mostrar_texto(superficie, nome, chave, pos_y):
    total = round(psutil.disk_usage('.').total / (1024 * 1024 * 1024), 2)
    used = round(psutil.disk_usage('.').used / (1024 * 1024 * 1024), 2)
    free = round(psutil.disk_usage('.').free / (1024 * 1024 * 1024), 2)
    percent = psutil.disk_usage('.').percent
    text = font.render(nome, True, Cores.branco)
    superficie.blit(text, (20, pos_y))

    if chave == 'total':
        s = f"{str(total)}GB"
    elif chave == 'used':
        s = f"{str(used)}GB - {str(percent)}%"
    elif chave == 'free':
        s = f"{str(free)}GB"
    else:
        s = psutil.disk_usage('.').chave
    text = font.render(s, True, Cores.cinza)
    superficie.blit(text, (160, pos_y))
