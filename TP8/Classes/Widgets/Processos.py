import psutil
import pygame

from Classes.Common import Cores
from Classes.Model import Processos, Arquivo

largura_tela = 800
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)
fontBold = pygame.font.SysFont('Segoe UI', 15, True)

pygame.display.init()

surface_processos = pygame.Surface((largura_tela, altura_tela))


def mostra_processos():
    surface_processos.fill(Cores.preto)
    processos = psutil.pids()
    processo = []
    processos.reverse()
    gap = 100
    numero_processos = 0

    for pid in processos:
        try:
            nome = psutil.Process(pid).name()
            tamanho_nome = len(nome)
            if pid != 1 and tamanho_nome <= 10:
                percent_uso = str(format(psutil.Process(pid).memory_percent(), '.2f')) + '%'
                memoria_usada = psutil.Process(pid).memory_info().rss / 1024 / 1024

                aux = Processos.Processos(pid, nome, percent_uso, memoria_usada)
                processo.append(aux)
                numero_processos += 1
        except:
            print(f"Erro ao obter informações do processo: {pid}")

        if numero_processos == 15:
            break

    titulo_processos = 'Informações dos processos:'
    texto_tiulo = fontBold.render(titulo_processos, True, Cores.cinza)
    surface_processos.blit(texto_tiulo, (20, 20))

    nome = '{:>5}'.format('PROCESSO')
    mem_usada = '{:>40}'.format('MEMÓRIA USADA')
    porcentagem = '{:>30}'.format('% DE USO')
    process_pid = '{:>30}'.format('PID')
    titulo_pid = nome + mem_usada + porcentagem + process_pid
    fonte_titulo = fontBold.render(titulo_pid, True, Cores.cinza)
    surface_processos.blit(fonte_titulo, (20, 65))

    for procs in processo:
        text_nome = '{:>0}'.format(Arquivo.Arquivo.ajusta_nome_arquivo(procs.nome))
        text_memoria_usada = '{:>40}'.format(str(format(procs.memoria_usada, '.2f'))) + 'MB'
        text_percentual_uso = '{:>45}'.format(procs.percent_uso)
        text_pid = '{:>40}'.format(Arquivo.Arquivo.ajusta_nome_arquivo(str(procs.pid)))
        text = text_nome + text_memoria_usada + text_percentual_uso + text_pid
        texto = font.render(text, True, Cores.cinza)
        surface_processos.blit(texto, (20, gap))

        gap += 25

    instrucao = font.render('Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.', True, Cores.branco)
    surface_processos.blit(instrucao, (150, 560))

    return surface_processos
