import pygame
from Classes.Widgets import CPU, Memoria, Disco, Redes, Resumo_Telas, Arquivo, Processos


pygame.display.set_caption("Gerenciador")
tela = pygame.display.set_mode((800, 600))
relogio = pygame.time.Clock()
terminou = False
count = 60
surface = 0
surfaces = [CPU.mostra_uso_cpu,
            Memoria.mostra_uso_memoria,
            Disco.mostrar_uso_disco,
            Redes.mostrar_info_ip_rede,
            Arquivo.mostra_arquivo,
            Processos.mostra_processos]
mostra_resumo = False

while not terminou:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminou = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if surface > 0:
                    surface -= 1
                else:
                    surface = len(surfaces) - 1

            if event.key == pygame.K_RIGHT:
                if surface < len(surfaces) - 1:
                    surface += 1
                else:
                    surface = 0

            if event.key == pygame.K_SPACE:
                mostra_resumo = not mostra_resumo

    if count == 60:
        if not mostra_resumo:
            tela.blit(surfaces[surface](), (0, 0))
            count = 0
        else:
            tela.blit(Resumo_Telas.resumo_telas(), (0, 0))
            count = 0

    pygame.display.update()

    relogio.tick(60)
    count += 1

pygame.display.quit()
