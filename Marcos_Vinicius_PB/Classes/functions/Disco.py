import psutil

from Classes.Model.Disco import Disco


def get_disk():
    total = round(psutil.disk_usage('.').total / (1024 * 1024 * 1024), 2)
    percent = psutil.disk_usage('.').percent
    used = round(psutil.disk_usage('.').used / (1024 * 1024 * 1024), 2)
    free = round(psutil.disk_usage('.').free / (1024 * 1024 * 1024), 2)

    disco = Disco(total, percent, used, free)
    return disco
