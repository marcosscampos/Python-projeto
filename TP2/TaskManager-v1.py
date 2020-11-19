import pygame
from Classes import Memoria, Disco, CPU, Rede

pygame.display.set_caption("Gerenciador de Tarefas")
relogio = pygame.time.Clock()
sair = False
cont = 60

while not sair:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sair = True
    if cont == 60:
        Memoria.mostra_uso_memoria()
        Disco.mostrar_uso_disco()
        CPU.mostra_uso_cpu()
        Rede.mostrar_info_ip_rede()
        cont = 0
    pygame.display.update()
    relogio.tick(60)
    cont += 1
pygame.display.quit()
