import pygame
import os
import time

from Classes.Common import Cores

largura_tela = 800
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_arquivo = pygame.surface.Surface((largura_tela, altura_tela))


def mostra_arquivo():
    surface_arquivo.fill(Cores.preto)
    arquivos = os.listdir()
    dic = {}

    for arquivo in arquivos:
        if os.path.isfile(arquivo):
            dic[arquivo] = []
            dic[arquivo].append(os.stat(arquivo).st_size)
            dic[arquivo].append(os.stat(arquivo).st_ctime)
            dic[arquivo].append(os.stat(arquivo).st_mtime)

    titulo = 'Informações de diretórios e arquivos:'
    nome_arquivo = '{:>10}'.format('Nome')
    data_criacao_arquivo = '{:>40}'.format('Data de Criação')
    data_modificacao_arquivo = '{:>45}'.format('Data de Modificação')
    tamanho_arquivo = '{:>50}'.format('Tamanho')
    diretorio_total = nome_arquivo + data_criacao_arquivo + data_modificacao_arquivo + tamanho_arquivo
    arquivo_titulo = font.render(titulo, True, Cores.cinza)
    surface_arquivo.blit(arquivo_titulo, (20, 10))
    arquivo_texto = font.render(diretorio_total, True, Cores.cinza)
    surface_arquivo.blit(arquivo_texto, (20, 50))

    x = 70
    for i in dic:
        kb = dic[i][0] / 1024
        nome = '{:>5}'.format(i)
        criacao = '{:>30}'.format(time.ctime(dic[i][0]))
        modificacao = '{:>35}'.format(time.ctime(dic[i][1]))
        tamanho = '{:>45}'.format(str('{:.2f}'.format(kb) + 'KB'))
        arquivo_texto_conteudo = font.render(nome + criacao + modificacao + tamanho, True, Cores.cinza)
        surface_arquivo.blit(arquivo_texto_conteudo, (15, x))
        x += 25

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_arquivo.blit(instrucao, (150, 560))

    return surface_arquivo
