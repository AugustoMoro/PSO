import Tkinter as tk
import ttk
from urllib import urlretrieve
import urllib2
import re
import os
import shutil
import string

class Application(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.grid()
		global canais
		global programacao
		global horario
		canais, programacao, horario = self.geraDados()
		self.set_widgets(canais, programacao, horario)
		self.titulo()
		self.botaoAtualizar()
		self.titulo1()
		self.entradaDados()
		self.botaoBuscar()

	#Label do primeiro titulo
	def titulo(self):
		self.titulo = ttk.Label(self.master, text="Programacao de TV")
		self.titulo["font"] =  ("Arial", "10", "bold")
		self.titulo.grid()

	#Label do segundo titulo
	def titulo1(self):
		self.titulo1 = ttk.Label(self.master, text="Digite um canal para buscar")
		self.titulo1["font"] =  ("Arial", "10", "bold")
		self.titulo1.grid()

	#Faz a entrada de dados para a busca de canais
	def entradaDados(self):
		self.text = ttk.Entry()
		self.text.grid()

	#Funcao que mostra e preenche a tabela de programacao
	def set_widgets(self, canais, programacao, horario):
		self.dataCols = ('Canal', 'Programa', 'Horario')
		self.tree = ttk.Treeview(columns=self.dataCols, show='headings')
		self.tree.column("Canal", width=200)
		self.tree.column("Programa", width=400)
		self.tree.column("Horario", width=100)
		self.tree.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)

		# Barras de rolagem
		ysb = ttk.Scrollbar(orient=tk.VERTICAL, command=self.tree.yview)
		xsb = ttk.Scrollbar(orient=tk.HORIZONTAL, command=self.tree.xview)
		self.tree['yscroll'] = ysb.set
		self.tree['xscroll'] = xsb.set
		ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
		xsb.grid(row=1, column=0, sticky=tk.E + tk.W)
		# Define o textos do cabecalho (nome em maiusculas)
		for c in self.dataCols:
			self.tree.heading(c, text=c.title())

		#dados
		self.data = []
		for i in range(len(canais)):
			self.data.append((canais[i], programacao[i], horario[i]))
		self.data.sort(key=lambda x: x[0])

		for item in self.data:
			self.tree.insert('', 'end', values=item)




	#Botao para atualizar a lista de canais
	def botaoAtualizar(self):
		self.botaoAtualizar = ttk.Button(self.master, command=self.actionBotaoOk)
		self.botaoAtualizar["text"] = "Atualizar"
		self.botaoAtualizar["width"] = 12
		self.botaoAtualizar.grid(row=3, column=0)

	#Botao para buscar os canais
	def botaoBuscar(self):
		self.botaoBuscar = ttk.Button(self.master, command=self.actionBotaoBusca)
		self.botaoBuscar["text"] = "Buscar"
		self.botaoBuscar["width"] = 12
		self.botaoBuscar.grid()

	#Funcao que pega o nome que deseja buscar
	def pegaNomeBusca(self):
		busca = self.text.get()
		return busca

	#Funcao que faz a busca quando o botao buscar e pressionado
	def actionBotaoBusca(self):
		busca = self.pegaNomeBusca()
		canalBusca, programacaoBusca, horarioBusca = self.buscaCanal(busca)
		self.set_widgets(canalBusca, programacaoBusca, horarioBusca)

	#Faz a busca de canais na lista 
	def buscaCanal(self, canalBusca):
		canalBuscado = []
		programacaoBuscada = []
		horarioBuscado = []
		for i in range(len(canais)):
			strCanal = canais[i].lower()
			canalBusca = canalBusca.lower()
			if string.find(strCanal, canalBusca, 0, len(canalBusca)) != -1:
				canalBuscado.append(canais[i])
				programacaoBuscada.append(programacao[i])
				horarioBuscado.append(horario[i])

		return (canalBuscado, programacaoBuscada, horarioBuscado)

	#Atualiza a tabela de canais quando o botao atualizar eeh pressionado
	def actionBotaoOk(self):
		global canais
		global programacao
		global horario
		canais, programacao, horario = self.geraDados()
		self.set_widgets(canais, programacao, horario)
		print "ok"

	#Gera os dados: canais, programacao e horario
	def geraDados(self):
		content = self.getHtml()
		canais = self.getCanais(content)
		programacao = self.getProgramacao(content)
		horario = self.getHorario(content)
		return (canais, programacao, horario)

	#pega o html da pagina
	def getHtml(self):
		url = "https://www.meuguia.tv/programacao/categoria/Todos"
		html = urllib2.urlopen(url)
		content = html.read()
		return content

	#pega a programacao
	def getProgramacao(self, content):
		programacaoSplit = content.split("class='prog_comp_tit'>")
		programacao = []
		for i in range(len(programacaoSplit)):
			if i != 0:
				aux = programacaoSplit[i]
				aux1 = ""
				cont = 0
				while aux[cont] != "<":
					aux1 = aux1 + aux[cont]
					cont = cont + 1
				aux1 = aux1.replace("&amp;", "&")
				aux1 = aux1.replace("&#39;", "'")
				programacao.append(aux1)
		return programacao

	#pega os canais 
	def getCanais(self, content):
		canalSplit = content.split("</strong> | ")
		canal = []
		for i in range(len(canalSplit)):
			if i != 0:
				aux = canalSplit[i]
				aux1 = ""
				cont = 0
				while aux[cont] != "<":
					aux1 = aux1 + aux[cont]
					cont = cont + 1
				aux1 = aux1.replace("&amp;", "&")
				aux1 = aux1.replace("&#39;", "'")
				canal.append(aux1)
		return canal

	#pega o horario
	def getHorario(self, content):
		horarioSplit = content.split("class='metadados'><strong>")
		horario = []
		for i in range(len(horarioSplit)):
			if i != 0:
				aux = horarioSplit[i]
				aux1 = ""
				cont = 0
				while aux[cont] != "<":
					aux1 = aux1 + aux[cont]
					cont = cont + 1
				aux1 = aux1.replace("&amp;", "&")
				aux1 = aux1.replace("&#39;", "'")
				horario.append(aux1)
		return horario


if __name__ == '__main__':
	root = tk.Tk()
	canais = []
	programacao = []
	horario = []
	app = Application(master=root)
	app.mainloop()