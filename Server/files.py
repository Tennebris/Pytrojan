#!/usr/bin/python

def download_server(name):
    f = open(name,"r")
    dados = f.read()
    f.close()
    return dados
def upload_server(nome,dados):
	try:
		f = open(nome,"w")
		f.write(dados)
		f.close()
		return "[+] Upload concluido"
	except:
		return "[-] Upload falido"
