#!-*- coding:utf-8
import nclib
import os
import getpass
import sys
import readline
import glob
import files

############# variaveis ###############
opt = [
	"download",
	"upload",
	"cd",
	"ls",
	"help",
	"cat",
]
dire = [
	"/",
	"root",
	"home",
	"var",
	"usr",
]
server = nclib.Netcat(listen=("",2890))
if sys.platform.startswith("linux"):
	dir_dark = "/home/"+getpass.getuser()+"/Darknet2890/"
	download_path = "/home/"+getpass.getuser()+"/Darknet2890/downloads/"
else:
	dir_dark = "c:/users/"+getpass.getuser()+"/Darknet2890/"
	download_path = "c:/users/"+getpass.getuser()+"/Darknet2890/downloads/"

if not os.path.exists(download_path):
	os.mkdir(dir_dark)
	os.mkdir(download_path)

class cores:
	if sys.platform.startswith('linux'):
		DARKCYAN = '\033[36m'
		ENDC = '\033[0m'
	else:
		DARKCYAN = ''
		ENDC = ''
	
readline.parse_and_bind("tab: complete")
def prompt():
	server.send("prompt")
	return server.read()
def esperar():
	try:
		while True:
			if server:
				global enviar
				global msg
				msg = server.read()
				if msg != None:
					print(msg)
				msg = None
				enviar = raw_input(prompt())
				readline.add_history(enviar)
				if "baixar" in enviar:
					server.send(enviar)
					dados = server.read()
					nome = enviar.replace("baixar ","")
					files.upload_server(download_path+nome,dados)
					print "salvado em "+download_path 
					server.send("#")
				elif "upload" in enviar:
					arq = enviar.replace("upload ","")
					dados = files.download_server(arq)
					server.send(enviar)
					server.send(dados)
				else:
					server.send(enviar)
	except KeyboardInterrupt:
		server.close()
		if sys.platform.startswith("linux"):
			os.system("clear")
		else:
			os.system("cls")
		sys.exit()
if __name__=="__main__":
	esperar()
