import psutil
import pygame

from Classes.Common import Cores
from Classes.Common.ClientSide import Client
from Classes.Model.Arquivo import Arquivo

client = Client.instance()
network = client.use('network')
memoria = client.use('memory')
disco = client.use('disk')

largura_tela = 800
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_resumo = pygame.surface.Surface((largura_tela, altura_tela))


def resumo_telas():
    surface_resumo.fill(Cores.preto)
    ##CPU
    porcentagem = psutil.cpu_percent(interval=0)
    largura = largura_tela - 2 * 20

    pygame.draw.rect(surface_resumo, Cores.azul_claro, (20, 40, largura, 50))
    tela.blit(surface_resumo, (20, 10))

    largura = largura * porcentagem / 100
    pygame.draw.rect(surface_resumo, Cores.azul, (20, 40, largura, 50))
    tela.blit(surface_resumo, (20, 10))

    text = font.render(f"Uso de CPU: {porcentagem}%", 1, Cores.branco)
    surface_resumo.blit(text, (20, 10))

    ##Disco
    largura = largura_tela - 2 * 20
    pygame.draw.rect(surface_resumo, Cores.verde_claro, (20, 130, largura, 50))
    tela.blit(surface_resumo, (0, 300))

    largura = largura * disco.percent / 100
    pygame.draw.rect(surface_resumo, Cores.verde, (20, 130, largura, 50))
    tela.blit(surface_resumo, (0, 300))

    texto_barra = f"Uso de disco: (Total: {str(disco.total)}GB" \
                  f" - {str(disco.percent)}% " \
                  f"- {str(disco.free)}GB)"
    text = font.render(texto_barra, 1, Cores.branco)
    surface_resumo.blit(text, (20, 100))

    ##memória
    largura = largura_tela - 2 * 20

    pygame.draw.rect(surface_resumo, Cores.roxo_claro, (20, 225, largura, 50))
    tela.blit(surface_resumo, (0, 140))

    largura = largura * memoria.percent / 100
    pygame.draw.rect(surface_resumo, Cores.roxo, (20, 225, largura, 50))
    tela.blit(surface_resumo, (0, 140))

    texto_barra = f"Uso de memória (Total: {str(memoria.total)}GB" \
                  f" - {str(memoria.percent)}%" \
                  f" - {str(memoria.used)}GB):"
    text = font.render(texto_barra, 1, Cores.branco)
    surface_resumo.blit(text, (20, 195))

    ##Rede
    texto_rede = font.render("Informações de Rede:", True, Cores.cinza)
    surface_resumo.blit(texto_rede, (20, 290))
    hosts = network
    aux = hosts
    gap = 320
    for host in aux:
        ip = str(host.ip)
        if ip != '127.0.0.1' and ip[0:3] != '169' and ip[0:3] != '172' \
                and host.pacotes[1][0] != '0' and host.pacotes[1][1] != 0:
            texto = font.render(Arquivo.ajusta_nome_arquivo(host.interface) + " - " + host.ip, True, Cores.cinza)

            surface_resumo.blit(texto, (20, gap))
            gap += 25

    instrucao = font.render(
        'Para voltar para as telas detalhadas, aperte ESPAÇO novamente.',
        True,
        Cores.branco)
    surface_resumo.blit(instrucao, (170, 560))

    return surface_resumo
