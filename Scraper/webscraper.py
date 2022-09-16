from os import link
from pickle import TRUE
import sys
import time
from tokenize import Double
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

destinos = {}

def __init__(self, link):
	self.link = link

def extrair_inteiro(texto):
	try:
		i = texto.rindex(' ')
		sem_unidade = texto[:i]

		# Às vezes, esse valor pode iniciar pelo ano...
		i = sem_unidade.find(' ')
		if i >= 0:
			sem_unidade = sem_unidade[(i + 1):]

		sem_virgula = sem_unidade.replace(',', '')

		return int(sem_virgula)
	except:
		return 0 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome()


import sqlite3
conn = sqlite3.connect('VOO_DB.db')
cursor = conn.cursor()

cursor.execute("""
create table if not exists voo (
idVoo int NOT NULL,
duracao int NOT NULL,
dataVoo datetime not null,
primary key(idVoo)
)
""")

cursor.execute("""
create table if not exists passagem(
idPassagem int not null,
companhia varchar(20) not null,
dataVisualizacao date not null,
precoPesquisa number(5,2) not null,
precoDesc number(5,2) null,
tpVoo varchar(15) not null,
idVoo_FK int not null,
primary key(idPassagem),
FOREIGN KEY (idVoo_FK) REFERENCES voo(idVoo)
)
""")

cursor.execute("""
create table if not exists destino(
idDestino int not null,
aeroporto varchar(3) not null,
cidade varchar(50) not null,
estado varchar(50) not null,
chegada datetime not null,
primary key(idDestino)
)
""")

#cursor.execute("""
#create table if not exists origem(
#idOrigem int not null,
#aeroporto varchar(3) not null,
#cidade varchar(50) not null,
#estado varchar(50) not null,
#saida datetime not null,
#primary key(idDestino)
#)
#""")

conn.commit()
conn.close()


lista = ['BSB','GIG','SSA','FLN','POA','REC','CWB','SDU','FOR','GYN','NVT','NAT','MCZ','FEN']
for destinos in lista:
	driver.get(f'https://www.latamairlines.com/br/pt/oferta-voos?origin=GRU&inbound=null&outbound=2022-12-01T15%3A00%3A00.000Z&destination={destinos}&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED')
	driver.maximize_window()
	# Cookie
	cookiebtn = WebDriverWait(driver, 40).until(
		EC.presence_of_element_located((By.ID, "cookies-politics-button"))
	)
	cookiebtn.click()

	valor_final = 0
	i=0
	while TRUE:
		tp_voo = driver.find_element(By.XPATH ,f'//*[@id="itinerary-modal-{i}-dialog-open"]/span').text
		if tp_voo =="Direto":
			valor = driver.find_element(By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[2]/div[2]/div/div/div/span/span[2]').get_attribute('innerHTML')
			print(valor)     
			valor_final += float(valor.replace(',','.'))            							
			i=i+1										
		else:
			break;	

	valor_final /=i
	print(f"Média de preço = {valor_final}")	
	#//*[@id="itinerary-modal-0-dialog-open"]
	#//*[@id="itinerary-modal-1-dialog-open"]

	#dados = []

	#""" for v in voos:
	#	dados.append({
	#		'destino': imagem.get_attribute('alt'),
	#		'hsaida': int(imagem.get_attribute('width')),
	#		'hchegada': int(imagem.get_attribute('height')),
	#		'duracao':,
	#		'valor':
	#	}) """

	#print(dados)
	
	driver.close()

	


	# Tela 1
	# Origem
	#origem = WebDriverWait(driver, 20).until(
	#	EC.presence_of_element_located((By.ID, "undefined-dialog-open"))
	#)

	#origem.send_keys('São Paulo, GRU - Brasil')
	#origem.send_keys(Keys.RETURN)

	#input = WebDriverWait(driver, 20).until(
	#	EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="q"]'))
	#)

	#voos = WebDriverWait(driver, 20).until(
	#	EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.rg_i'))
	#)