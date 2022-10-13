from datetime import date
import datetime
from os import link
from pickle import FALSE, TRUE
import sys
import time
from timeit import Timer
from tokenize import Double
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from storage import *

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

def main(lista):
	cookie = False
 
	for destinos in lista:
		driver.get(f'https://www.latamairlines.com/br/pt/oferta-voos?origin=GRU&inbound=null&outbound=2022-12-01T15%3A00%3A00.000Z&destination={destinos}&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED')
		driver.maximize_window()
		time.sleep(30)
		# Verifica se há Cookie e aceita ele
		if cookie == False:
			cookiebtn = WebDriverWait(driver, 30).until(
				EC.presence_of_element_located((By.ID, "cookies-politics-button"))
			)
			cookie = True
			cookiebtn.click()
	
		#def check():
		#	try:
		#		WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,'//*[@id="itinerary-modal-0-dialog-open"]/span')))
		#		return FALSE
		#	except NoSuchElementException:
		#		return TRUE
		#timer = check()
		#WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,'//*[@id="itinerary-modal-0-dialog-open"]/span')))
			
		#Selecionando os destinos e a origem e inserindo na tabela de voo
		# origem= driver.find_element(By.XPATH ,'//*[@id="txtInputOrigin_field"]').get_attribute('value')
		# origem = 'São Paulo, GRU - Brasil'
		destino= driver.find_element(By.XPATH ,'//*[@id="txtInputDestination_field"]').get_attribute('value')
		# inserirVoo(origem, destino)
		# print(destino)
		
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

					if float(valor) >= float(maior):
						maior = float(valor)
						maiorI = i
					else:
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
		companhia = 'LATAM'
		dataVoo = '2022-12-01'
		dataPesquisa = datetime.datetime.now().date()
		idVoo = obterIdVoo(destino)
		inserirPassagem(idVoo[0],companhia,valor_final,dataVoo,str(dataPesquisa))

		idPassagem = obterIdPassagem(idVoo[0], str(dataPesquisa))

		i = maiorI 
		for j in range(2):
			hSaida = driver.find_element(By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[1]/div[1]/span[1]').text
			hChegada =  driver.find_element(By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[1]/div[3]/span[1]').text
   
			if "+" in hChegada:
				hChegada = hChegada[:-2]
			duracao =  driver.find_element(By.XPATH ,f'//*[@id="ContainerFlightInfo{i}"]/span[2]').text
			h1 = duracao[0:2].strip()
			h2 = duracao[-7:-5].replace(" ", "0")

			if len(h1) == 1:
				h1 = '0' + h1

			duracao = h1 +':' + h2
	
			preco =  driver.find_element(By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[2]/div/div/span/span[2]').text
			preco = preco.replace('.','')
			preco = preco.replace(',','.')
			#print(preco)
			#print(float(preco))

			inserirTpPassagem(idPassagem[0],hSaida ,hChegada, duracao ,preco)
			i = menorI
		
		print(destino)
		print(valor_final)
		

	driver.close()
 
if __name__ == '__main___':
    main()