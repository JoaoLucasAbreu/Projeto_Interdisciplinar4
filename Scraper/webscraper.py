from datetime import date
import datetime
from os import link
from pickle import FALSE, TRUE
import sys
import time
from tokenize import Double
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sqlite3
conn = sqlite3.connect('VOO_DB.db')
cursor = conn.cursor()

cursor.execute("""
create table if not exists voo (
idVoo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
origem TEXT NOT NULL,
destino TEXT NOT NULL
)
""")

cursor.execute("""
create table if not exists passagem(
idPassagem INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
idVoo INTEGER NOT NULL,
companhia TEXT NOT NULL,
media DOUBLE(5,2) NOT NULL,
dataVoo TEXT not null,
dataPesquisa TEXT not null,
FOREIGN KEY(idVoo) REFERENCES voo(idVoo)
)
""")

cursor.execute("""
create table if not exists tp_passagem(
idTpPassagem INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
idPassagem INTEGER NOT NULL,
hSaida TEXT NOT NULL,
hChegada TEXT NOT NULL,
duracao TEXT NOT NULL,
preco DOUBLE(5,2) NOT NULL,
FOREIGN KEY(idPassagem) REFERENCES passagem (idPassagem)
)
""")

conn.commit()
conn.close()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

cookie = False
lista = ['BSB','GIG','SSA','FLN','POA','REC','CWB','SDU','FOR','GYN','NVT','NAT','MCZ']
for destinos in lista:
	driver.get(f'https://www.latamairlines.com/br/pt/oferta-voos?origin=GRU&inbound=null&outbound=2022-12-01T15%3A00%3A00.000Z&destination={destinos}&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED')
	driver.maximize_window()

	# Verifica se há Cookie e aceita ele
	if cookie == False:
		cookiebtn = WebDriverWait(driver, 30).until(
			EC.presence_of_element_located((By.ID, "cookies-politics-button"))
		)
		cookie = True
		cookiebtn.click()

	def check():
		try:
			driver.find_element(By.XPATH ,'//*[@id="itinerary-modal-0-dialog-open"]/span')
			return FALSE
		except NoSuchElementException:
			return TRUE
	
	timer = FALSE
	timer = check()
	if timer == TRUE:
		time.sleep(40)
		print('tinha timer')

	#Selecionando os destinos e a origem e inserindo na tabela de voo
	conn = sqlite3.connect('VOO_DB.db')
	cursor = conn.cursor()
	origem= driver.find_element(By.XPATH ,'//*[@id="txtInputOrigin_field"]').get_attribute('value')
	destino= driver.find_element(By.XPATH ,'//*[@id="txtInputDestination_field"]').get_attribute('value')
	cursor.execute('INSERT INTO voo(origem, destino) VALUES (?,?)', (origem, destino))
	conn.commit()
	conn.close()


	valor_final = 0
	i=0
	try:
		maior = driver.find_element(By.XPATH ,'//*[@id="WrapperCardFlight0"]/div/div[2]/div[2]/div/div/div/span/span[2]').get_attribute('innerHTML')
		menor = driver.find_element(By.XPATH ,'//*[@id="WrapperCardFlight0"]/div/div[2]/div[2]/div/div/div/span/span[2]').get_attribute('innerHTML')
		maior = maior.replace('.','')
		maior = maior.replace(',','.')
		menor = menor.replace('.','')
		menor = menor.replace(',','.')
		maiorI = 0
		menorI = 0
	except NoSuchElementException:
			break

	while TRUE:		
		try:			
			tp_voo = driver.find_element(By.XPATH ,f'//*[@id="itinerary-modal-{i}-dialog-open"]/span').text
			if tp_voo =="Direto":				
				valor = driver.find_element(By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[2]/div[2]/div/div/div/span/span[2]').get_attribute('innerHTML')     
				valor = valor.replace('.','')
				valor = valor.replace(',','.')

				if float(valor) > float(maior):
					maior = float(valor)
					maiorI = i

				if float(valor) < float(menor):
					menor = float(valor)	
					menorI = i

				valor_final += float(valor)   
				duracao = driver.find_element(By.XPATH ,f'//*[@id="ContainerFlightInfo{i}"]/span[2]').get_attribute('innerHTML')     							
				i+=1		
			else:
				break;	
		except NoSuchElementException:
			break
	if i >0:
		valor_final /=i
	
	#Inserindo dados gerais sobre a passagem 
	conn = sqlite3.connect('VOO_DB.db')
	cursor = conn.cursor()
	companhia = 'LATAM'
	dataVoo = driver.find_element(By.XPATH ,'//*[@id="departureDate"]').get_attribute('value')
	
	dataPesquisa = datetime.datetime.now().date()
	print(dataPesquisa)
	idVoo = cursor.execute('SELECT (idVoo) from voo WHERE destino = ?',[(destino)]).fetchone()
	cursor.execute('INSERT INTO passagem(idVoo,companhia,media,dataVoo,dataPesquisa) VALUES (?,?,?,?,?)', (idVoo[0],companhia,valor_final,dataVoo,str(dataPesquisa)))
	conn.commit()
	conn.close()

	conn = sqlite3.connect('VOO_DB.db')
	cursor = conn.cursor()
	idPassagem = cursor.execute('SELECT (idPassagem) from passagem WHERE idVoo =? AND dataPesquisa=?', (idVoo[0], str(dataPesquisa))).fetchone()
	conn.commit()
	conn.close()

	i = maiorI
	for j in range(2):
		conn = sqlite3.connect('VOO_DB.db')
		cursor = conn.cursor()
		hChegada = driver.find_element(By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[1]/div[1]/span[1] ').text
		hSaida =  driver.find_element(By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[1]/div[3]/span[1]').text
		duracao =  driver.find_element(By.XPATH ,f'//*[@id="ContainerFlightInfo{i}"]/span[2]').text
		preco =  driver.find_element(By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[2]/div/div/span/span[2]').text
		print(hChegada)
		print(hSaida)
		print(duracao)
		print(preco)
		cursor.execute('INSERT INTO tp_passagem(idPassagem,hSaida ,hChegada,duracao ,preco) VALUES (?,?,?,?,?)', (idPassagem[0],hSaida ,hChegada,duracao ,preco))
		i= menorI
		conn.commit()
		conn.close()


driver.close()

