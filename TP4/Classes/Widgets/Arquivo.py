import pygame
import os
import time

from Classes.Common import Cores
from Classes.Model.Arquivo import Arquivo

largura_tela = 800
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)
fontBold = pygame.font.SysFont('Segoe UI', 15, True)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_arquivo = pygame.surface.Surface((largura_tela, altura_tela))


def mostra_arquivo():
    surface_arquivo.fill(Cores.preto)
    arquivos = os.listdir(".")
    exibicao = 0
    dic = {}

    for arquivo in arquivos:
        dic[arquivo] = []
        dic[arquivo].append(os.stat(arquivo).st_size)
        dic[arquivo].append(os.stat(arquivo).st_mtime)

    titulo = 'Informações de diretórios e arquivos:'
    nome_arquivo = '{:>10}'.format('Nome')
    data_modificacao_arquivo = '{:>80}'.format('Data de Modificação')
    tamanho_arquivo = '{:>45}'.format('Tamanho')
    diretorio_total = nome_arquivo + data_modificacao_arquivo + tamanho_arquivo
    arquivo_titulo = font.render(titulo, True, Cores.cinza)
    surface_arquivo.blit(arquivo_titulo, (20, 10))
    arquivo_texto = fontBold.render(diretorio_total, True, Cores.cinza)
    surface_arquivo.blit(arquivo_texto, (20, 50))

    x = 80
    for i in dic:
        if exibicao <= 15:
            nome = Arquivo.ajusta_nome_arquivo(i)
            modificacao = '{:>80}'.format(time.ctime(dic[i][1]))
            tamanho = '{:>45}'.format(str('{:.2f}'.format(dic[i][0] / 1024) + 'KB'))
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
