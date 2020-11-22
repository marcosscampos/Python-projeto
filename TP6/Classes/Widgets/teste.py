import os
import subprocess
import nmap
from platform import system

import psutil


def ping(address: str):
    platform = system()

    if platform == 'Windows':
        args = ['ping', '-n', '1', '-l', '1', '-w', '100', address]
    else:
        args = ['ping', '-c', '1', '-W', '1', address]

    return subprocess.call(args,
                           stdout=open(os.devnull, 'w'),
                           stderr=open(os.devnull, 'w'))


def verify_hosts(base: str):
    print('Mapping')
    valid_hosts = []
    codes = dict()

    for i in range(1, 255):
        codes[f'{base}{i}'] = ping(f'{base}{i}')

        if i % 20 == 0:
            print('.', end='')
        if codes[f'{base}{i}'] == 0:
            valid_hosts.append(f'{base}{i}')
    print('\nMapping ready...')

    return valid_hosts


ip_info = psutil.net_if_addrs()
ip = ip_info['Wi-Fi'][1].address


base_ip = '.'.join(ip.split('.')[0:3]) + '.'
print(base_ip)
print('Os hosts válidos são: ', verify_hosts(base_ip))

def ports(host: str):
    nm = nmap.PortScanner()
    nm.scan(host)
    ports = []

    for proto in nm[host].all_protocols():

        lport = nm[host][proto].keys()

        for port in lport:
            ports.append({
                'port': port,
                'state': nm[host][proto][port]["state"]
            })

    return ports