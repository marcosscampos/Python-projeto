import psutil
import pygame
import time

from Classes.Common import Cores
from Classes.Model import Processos

largura_tela = 800
altura_tela = 600

pygame.font.init()
font = pygame.font.SysFont('Segoe UI', 15)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.init()

surface_processos = pygame.Surface((largura_tela, altura_tela))


def mostra_processos():
    processos = psutil.pids()
    processo = []
    gap = 70
    numero_processos = 0

    for pid in processos:
        try:
            nome = psutil.Process(pid).name()
            percent_uso = psutil.Process(pid).cpu_percent()
            memoria_usada = psutil.Process(pid).memory_info().rss / 1024 / 1024
            threads_usadas = psutil.Process(pid).num_threads()
            tempo_uso = str(psutil.Process(pid).cpu_times().user) + ' s'
            data_criacao = time.ctime(psutil.Process(pid).create_time())

            aux = Processos.Processos(pid, nome, percent_uso, memoria_usada, threads_usadas, tempo_uso, data_criacao)
            processo.append(aux)
            numero_processos += 1
        except:
            print(f"Erro ao obter informações do processo: {pid}")

        if numero_processos == 10:
            break

    titulo_processos = 'Informações dos processos:'
    texto_tiulo = font.render(titulo_processos, True, Cores.cinza)
    surface_processos.blit(texto_tiulo, (20, 20))
    process_pid = '{:>5}'.format('PID')
    tempo = '{:>20}'.format('Tempo de Uso')
    threads = '{:>20}'.format('Threads')
    mem_usada = '{:>20}'.format('Memória Usada')
    porcentagem = '{:>20}'.format('% de uso')
    nome = '{:>30}'.format('Processo')
    titulo_pid = process_pid + tempo + threads + mem_usada + porcentagem + nome
    fonte_titulo = font.render(titulo_pid, True, Cores.cinza)
    surface_processos.blit(fonte_titulo, (20, 50))

    for procs in processo:
        text_pid = '{:>5}'.format(str(procs.pid))
        text_tempo = '{:>25}'.format(procs.tempo_uso, '.2f')
        text_threads_processo = '{:>30}'.format(procs.threads_usadas)
        text_memoria_usada = '{:>25}'.format(str(format(procs.memoria_usada, '.2f')))
        text_percentual_uso = '{:>22}'.format(str(format(procs.percent_uso, '.2f')))
        text_nome = '{:>35}'.format(procs.nome)
        texto_formatado = text_pid + text_tempo + text_threads_processo \
                          + text_memoria_usada + text_percentual_uso + text_nome
        texto = font.render(texto_formatado, True, Cores.cinza)
        surface_processos.blit(texto, (20, gap))

        gap += 25

    instrucao = font.render(
        'Tecle ← ou → para navegar. Para ver o resumo, aperte a tecla ESPAÇO.',
        True,
        Cores.branco)
    surface_processos.blit(instrucao, (150, 560))

    return surface_processos
