import psutil
import pygame

from Classes.Common import Cores
from Classes.Common.ClientSide import Client

largura_tela = 800
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_memoria = pygame.Surface((largura_tela, altura_tela))


def mostra_uso_memoria():
    largura = largura_tela - 2 * 20
    surface_memoria.fill(Cores.preto)
    pygame.draw.rect(surface_memoria, Cores.roxo_claro, (20, 140, largura, 50))

    largura = largura * psutil.virtual_memory().percent / 100
    pygame.draw.rect(surface_memoria, Cores.roxo, (20, 140, largura, 50))
    tela.blit(surface_memoria, (0, 140))

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_memoria.blit(instrucao, (150, 560))

    mostra_texto(surface_memoria, 'Memória Total: ', 'total', 55)
    mostra_texto(surface_memoria, 'Memória Em Uso: ', 'used', 80)
    mostra_texto(surface_memoria, 'Memória Livre: ', 'free', 105)
    tela.blit(surface_memoria, (0, 150))

    return surface_memoria


def mostra_texto(superficie, nome, chave, pos_y):
    text = font.render(nome, True, Cores.branco)
    superficie.blit(text, (20, pos_y))
    cliente = Client.instance()
    memoria = cliente.use('memory')

    if chave == 'total':
        s = f"{str(memoria.total)}GB"
    elif chave == 'used':
        s = f"{str(memoria.used)}GB - {memoria.percent}%"
    elif chave == 'free':
        s = f"{str(memoria.free)}GB"
    text = font.render(s, True, Cores.cinza)
    superficie.blit(text, (160, pos_y))
