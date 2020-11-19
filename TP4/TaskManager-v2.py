import pygame
from Classes.Widgets import CPU, Memoria, Disco, Redes, Resumo_Telas

pygame.display.set_caption("Gerenciador")
tela = pygame.display.set_mode((600, 600))
relogio = pygame.time.Clock()
running = True
cont = 60
surface = 0
surfaces = [CPU.mostra_uso_cpu,
            Memoria.mostra_uso_memoria,
            Disco.mostrar_uso_disco,
            Redes.mostrar_info_ip_rede]
mostra_resumo = False

while running:
    relogio.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    if cont == 60:
        if not mostra_resumo:
            tela.blit(surfaces[surface](), (0, 0))
        else:
            tela.blit(Resumo_Telas.resumo_telas(), (0, 0))
        cont = 0
    pygame.display.update()
    cont += 1
pygame.display.quit()
