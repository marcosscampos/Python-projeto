class Arquivo:
    def __init__(self, nome_arquivo, data_modificacao, tamanho):
        self.nome_arquivo = nome_arquivo
        self.data_modificacao = data_modificacao
        self.tamanho = tamanho

    @classmethod
    def ajusta_nome_arquivo(cls, nome):
        aux = nome
        tamanho_minimo = 10
        palavra_tamanho = len(aux)

        if palavra_tamanho > tamanho_minimo:
            aux = '{:.10}'.format(nome)
        else:
            while palavra_tamanho != tamanho_minimo:
                aux += " "
                palavra_tamanho = len(aux)

        return aux
