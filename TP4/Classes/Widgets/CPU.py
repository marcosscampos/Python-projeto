import psutil
import pygame
import cpuinfo

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Verdana', 15)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_cpu = pygame.Surface((largura_tela, altura_tela))
info_cpu = cpuinfo.get_cpu_info()


def mostra_uso_cpu():
    surface_cpu.fill(Cores.preto)
    mostra_texto(surface_cpu, "Nome:", "brand_raw", 10)
    mostra_texto(surface_cpu, "Arquitetura:", "arch", 30)
    mostra_texto(surface_cpu, "Versão (bits):", "bits", 50)
    mostra_texto(surface_cpu, "Frequência (MHz):", "freq", 70)
    mostra_texto(surface_cpu, "Núcleos (físicos):", "nucleos", 90)
    tela.blit(surface_cpu, (20, 150))

    capacidade = psutil.cpu_percent(interval=1, percpu=True)

    qtd_cpu = len(capacidade)
    x = y = 10
    deslocamento = 15
    altura = surface_cpu.get_height() - 150
    largura = (surface_cpu.get_width() - 2 * y - (qtd_cpu + 1) * deslocamento) / qtd_cpu
    d = x + deslocamento
    for i in capacidade:
        pygame.draw.rect(surface_cpu, Cores.azul, (d, 140, largura, altura))
        pygame.draw.rect(surface_cpu, Cores.azul_claro, (d, 140, largura, (1 - i / 100) * altura))
        d = d + largura + deslocamento
    tela.blit(surface_cpu, (1, altura_tela / 5))

    return surface_cpu


def mostra_texto(s1, nome, chave, pos_y):
    text = font.render(nome, True, Cores.branco)
    s1.blit(text, (10, pos_y))
    if chave == "freq":
        s = f"{str(round(psutil.cpu_freq().current, 2))} - {psutil.cpu_percent(interval=0)}%"
    elif chave == "nucleos":
        s = str(psutil.cpu_count())
        s += f" ({str(psutil.cpu_count(logical=False))})"
    else:
        s = str(info_cpu[chave])
    text = font.render(s, True, Cores.cinza)
    s1.blit(text, (160, pos_y))