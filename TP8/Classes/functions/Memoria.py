import psutil

from Classes.Model.Memoria import Memoria


def set_memoria():
    memo = psutil.virtual_memory()

    total = round(memo.total / (1024 * 1024 * 1024), 2)
    percent = memo.percent
    used = round(memo.used / (1024 * 1024 * 1024), 2)
    free = round(memo.free / (1024 * 1024 * 1024), 2)
    memory = Memoria(total, percent, used, free)

    return memory
