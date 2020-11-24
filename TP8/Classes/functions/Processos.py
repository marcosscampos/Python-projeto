import psutil
from Classes.Model.Processos import Processos


def set_processos():
    processos = sorted(psutil.pids(), reverse=True)
    numero_processos = 0
    processo = []

    for pid in processos:
        try:
            nome = psutil.Process(pid).name()
            tamanho_nome = len(nome)
            if pid != 1 and tamanho_nome <= 10:
                percent_uso = str(format(psutil.Process(pid).memory_percent(), '.2f')) + '%'
                memoria_usada = psutil.Process(pid).memory_info().rss / 1024 / 1024

                aux = Processos(pid, nome, percent_uso, memoria_usada)
                processo.append(aux)
                numero_processos += 1
        except:
            print(f"Erro ao obter informações do processo: {pid}")

        if numero_processos == 15:
            break
    return processo
