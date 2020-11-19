class Processos:
    def __init__(self, pid, nome, percent_uso, memoria_usada, threads_usadas, tempo_uso, data_criacao):
        self.pid = pid
        self.nome = nome
        self.percent_uso = percent_uso
        self.memoria_usada = memoria_usada
        self.threads_usadas = threads_usadas
        self.tempo_uso = tempo_uso
        self.data_criacao = data_criacao
