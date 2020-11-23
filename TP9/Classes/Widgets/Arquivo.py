import pygame
import os
import time
import sched
import threading

from Classes.Common import Cores
from Classes.Model.Arquivo import Arquivo

largura_tela = 800
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)
fontBold = pygame.font.SysFont('Segoe UI', 15, True)

pygame.display.init()

surface_arquivo = pygame.surface.Surface((largura_tela, altura_tela))
tempo_execucao = []
arquivos = {}


def mostra_arquivo():
    surface_arquivo.fill(Cores.preto)
    tempo_execucao = sched_arquivos()

    final = tempo_execucao[0]
    usado = tempo_execucao[1]

    texto_final = fontBold.render(final, True, Cores.cinza)
    surface_arquivo.blit(texto_final, (20, 480))
    texto_usado = fontBold.render(usado, True, Cores.cinza)
    surface_arquivo.blit(texto_usado, (20, 500))

    exibicao = 0

    titulo = 'Informações de diretórios e arquivos:'
    nome_arquivo = '{:>10}'.format('Nome')
    data_modificacao_arquivo = '{:>80}'.format('Data de Modificação')
    tamanho_arquivo = '{:>45}'.format('Tamanho')

    diretorio_total = nome_arquivo + data_modificacao_arquivo + tamanho_arquivo
    arquivo_texto = fontBold.render(diretorio_total, True, Cores.cinza)
    surface_arquivo.blit(arquivo_texto, (20, 50))

    arquivo_titulo = fontBold.render(titulo, True, Cores.cinza)
    surface_arquivo.blit(arquivo_titulo, (20, 10))

    x = 80
    for i in arquivos:
        if exibicao <= 10:
            nome = Arquivo.ajusta_nome_arquivo(i)
            modificacao = '{:>80}'.format(time.ctime(arquivos[i][1]))
            tamanho = '{:>45}'.format(str('{:.2f}'.format(arquivos[i][0] / 1024) + 'KB'))
            arquivo_texto_conteudo = font.render(nome + modificacao + tamanho, True, Cores.cinza)
            surface_arquivo.blit(arquivo_texto_conteudo, (50, x))
            x += 25
            exibicao += 1

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_arquivo.blit(instrucao, (150, 560))

    return surface_arquivo


def listar_arquivos():
    arquivos_aux = os.listdir()
    for arquivo in arquivos_aux:
        arquivos[arquivo] = []
        arquivos[arquivo].append(os.stat(arquivo).st_size)
        arquivos[arquivo].append(os.stat(arquivo).st_mtime)


def sched_arquivos():
    inicio = time.time()
    clock_inicio = time.process_time()

    arquivo = sched.scheduler(time.time, time.sleep)
    arquivo.enter(4, 1, listar_arquivos)

    if len(arquivos) == 0:
        t = threading.Thread(target=arquivo.run())
        t.start()

    tempo_final = f'TEMPO FINAL {time.ctime()} | CLOCK FINAL: {str(format(time.process_time(), ".2f"))}'

    final = time.time() - inicio
    clock_final = time.process_time() - clock_inicio

    usado = f'TEMPO USADO NESSA CHAMADA: {str(format(final, ".2f"))} ' \
            f'| CLOCK USADO NESSA CHAMADA: {str(format(clock_final, ".2f"))}'

    return tempo_final, usado
