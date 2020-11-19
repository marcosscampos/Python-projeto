import psutil
import pygame

from Classes.Common import Cores

largura_tela = 600
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_resumo = pygame.surface.Surface((largura_tela, altura_tela))


def mostrar_ips():
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            yield interface, snic.address


def get_ip():
    return list(mostrar_ips())


def resumo_telas():
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

    largura = largura * psutil.disk_usage('.').percent / 100
    pygame.draw.rect(surface_resumo, Cores.verde, (20, 130, largura, 50))
    tela.blit(surface_resumo, (0, 300))

    texto_barra = f"Uso de disco: (Total: {str(round(psutil.disk_usage('.').total / (1024 * 1024 * 1024), 2))}GB" \
                  f" - {str(psutil.disk_usage('.').percent)}% " \
                  f"- {str(round(psutil.disk_usage('.').used / (1024 * 1024 * 1024), 2))}GB)"
    text = font.render(texto_barra, 1, Cores.branco)
    surface_resumo.blit(text, (20, 100))

    ##memória
    largura = largura_tela - 2 * 20

    pygame.draw.rect(surface_resumo, Cores.roxo_claro, (20, 225, largura, 50))
    tela.blit(surface_resumo, (0, 140))

    largura = largura * psutil.virtual_memory().percent / 100
    pygame.draw.rect(surface_resumo, Cores.roxo, (20, 225, largura, 50))
    tela.blit(surface_resumo, (0, 140))

    texto_barra = f"Uso de memória (Total: {str(round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2))}GB" \
                  f" - {str(psutil.virtual_memory().percent)}%" \
                  f" - {str(round(psutil.virtual_memory().used / (1024 * 1024 * 1024), 2))}GB):"
    text = font.render(texto_barra, 1, Cores.branco)
    surface_resumo.blit(text, (20, 195))

    ##Rede
    texto_rede = font.render("Informações de Rede:", True, Cores.cinza)
    surface_resumo.blit(texto_rede, (20, 290))
    hosts = mostrar_ips()
    aux = hosts
    gap = 320
    for host in aux:
        ip = str(host[1])
        if ip != '127.0.0.1':
            texto = font.render(host[0] + ": " + host[1], 1, Cores.cinza)

            surface_resumo.blit(texto, (20, gap))
            gap += 25

    instrucao = font.render(
        'Para voltar para as telas detalhadas, aperte ESPAÇO novamente.',
        True,
        Cores.branco)
    surface_resumo.blit(instrucao, (80, 560))

    return surface_resumo
