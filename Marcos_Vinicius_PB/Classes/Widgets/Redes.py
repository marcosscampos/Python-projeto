import pygame

from Classes.Common import Cores
from Classes.Model import Arquivo
from Classes.Common.ClientSide import Client

client = Client.instance()
network = client.use('network')

largura_tela = 800
altura_tela = 600
pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)
fontBold = pygame.font.SysFont('Segoe UI', 15, True)
pygame.display.init()

surface_rede = pygame.surface.Surface((largura_tela, altura_tela))


def mostrar_info_ip_rede():
    surface_rede.fill(Cores.preto)
    texto = 'Informações De Rede:'
    texto_font = font.render(texto, True, Cores.cinza)
    surface_rede.blit(texto_font, (20, 20))

    aux = network
    gap = 85

    mostra_info_hosts_rede()

    nome = '{:>5}'.format('INTERFACE')
    ip = '{:>30}'.format('IP')
    mascara = '{:>43}'.format("MÁSCARA")
    pacote_enviado = '{:>28}'.format('PCT. ENVIADO')
    pacote_recebido = '{:>28}'.format('PCT. RECEBIDO')
    titulo_rede = nome + ip + mascara + pacote_enviado + pacote_recebido
    fonte_titulo_rede = fontBold.render(titulo_rede, True, Cores.cinza)
    surface_rede.blit(fonte_titulo_rede, (20, 65))

    for host in aux:
        ip = str(host.ip)
        if ip != '127.0.0.1' and ip[0:3] != '169' and ip[0:3] != '172'\
                and host.pacotes[1][0] != '0' and host.pacotes[1][1] != 0:
            texto_interface = '{:>0}'.format(Arquivo.Arquivo.ajusta_nome_arquivo(host.interface))
            texto_ip = '{:>38}'.format(host.ip)
            texto_mascara = '{:>40}'.format(str(host.mascara))
            texto_pacote_enviado = '{:>25}'.format(str(round(host.pacotes[1][0] / (1024 ** 2), 2))) + 'MB'  # Enviado
            texto_pacote_recebido = '{:>30}'.format(str(round(host.pacotes[1][1] / (1024 ** 2), 2))) + 'MB'  # Recebido
            texto_compilado = texto_interface + texto_ip + texto_mascara + texto_pacote_enviado + texto_pacote_recebido
            texto_tela = font.render(texto_compilado, True, Cores.cinza)
            surface_rede.blit(texto_tela, (20, gap))
            gap += 25

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_rede.blit(instrucao, (150, 560))

    return surface_rede


def mostra_info_hosts_rede():
    detailed_hosts = client.use('detailed_hosts')
    hosts_detalhados = detailed_hosts
    gap = 185

    for host_rede in hosts_detalhados:

        if host_rede.nome == "":
            host_rede.nome = "Nome não identificado."

        texto = font.render('IP:' + host_rede.ip + ' - Nome: ' + host_rede.nome, True, Cores.cinza)
        surface_rede.blit(texto, (20, gap))
        gap += 15

        for porta in host_rede.portas:
            if porta.portas != "" and porta.estado != "":
                texto_porta_estado = f'Porta: {str(porta.portas)} - Estado: {porta.estado}'
                textos = font.render(texto_porta_estado, True, Cores.cinza)
                surface_rede.blit(textos, (20, gap))
                gap += 20
        gap += 15
