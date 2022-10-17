from datetime import date
import datetime
from os import link
from pickle import FALSE, TRUE
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from storage import *

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--force-device-scale-factor=0.5")
driver = webdriver.Chrome(options=chrome_options)

def main(lista):
	cookie = False
	idVoo = 1
	for destinos in lista:
		driver.get(f'https://www.latamairlines.com/br/pt/oferta-voos?origin=GRU&inbound=null&outbound=2022-12-01T15%3A00%3A00.000Z&destination={destinos}&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED')
		driver.maximize_window()
		# Verifica se há Cookie e aceita ele
		if cookie == False:
			cookiebtn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "cookies-politics-button")))
			cookiebtn.click()
			cookie = True

		valor_final = 0
		i=0
		try:
			maior = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,'//*[@id="WrapperCardFlight0"]/div/div[2]/div[2]/div/div/div/span/span[2]')))
			maior = maior.get_attribute('innerHTML')
			menor = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,'//*[@id="WrapperCardFlight0"]/div/div[2]/div[2]/div/div/div/span/span[2]')))
			menor = menor.get_attribute('innerHTML')
			maior = maior.replace('.','')
			maior = maior.replace(',','.')
			menor = menor.replace('.','')
			menor = menor.replace(',','.')
			maiorI = 0
			menorI = 0
		except NoSuchElementException:
				break

		i = 0		
		while TRUE:		
			try:																								
				tp_voo = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,f'//*[@id="itinerary-modal-{i}-dialog-open"]/span')))
				tp_voo = tp_voo.text
				if tp_voo =="Direto":				
					valor = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[2]/div[2]/div/div/div/span/span[2]')))
					valor = valor.get_attribute('innerHTML')
					valor = valor.replace('.','')
					valor = valor.replace(',','.')

					if float(valor) >= float(maior):
						maior = float(valor)
						maiorI = i
					else:
						menor = float(valor)	
						menorI = i

					valor_final += float(valor)   
					duracao = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,f'//*[@id="ContainerFlightInfo{i}"]/span[2]')))
					duracao = duracao.get_attribute('innerHTML')						
					i+=1		
				else:
					break;	
			except NoSuchElementException:
				break

		if i >0:
			valor_final /=i
		else: 
			valor_final = maior	
		
		#Inserindo dados gerais sobre a passagem 
		companhia = 'LATAM'
		dataVoo = '2022-12-01'
		dataPesquisa = datetime.datetime.now().date()
		inserirPassagem(idVoo,companhia,valor_final,dataVoo,str(dataPesquisa))
		idPassagem = obterIdPassagem(idVoo, str(dataPesquisa))

		i = maiorI 
		time.sleep(10)
		for j in range(2):																		 
			hSaida = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[1]/div[1]/span[1]')))
			hSaida = hSaida.text
			if hSaida == '' or hSaida == ':': 
				print("ERRO")
    
			hChegada = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[1]/div[3]/span[1]')))
			hChegada = hChegada.text
   
			if "+" in hChegada:
				hChegada = hChegada[:-2]
			duracao = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,f'//*[@id="ContainerFlightInfo{i}"]/span[2]')))
			duracao = duracao.text
			h1 = duracao[0:2].strip()
			h2 = duracao[-7:-5].replace(" ", "0")

			if len(h1) == 1:
				h1 = '0' + h1

			duracao = h1 +':' + h2
	
			preco = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH ,f'//*[@id="WrapperCardFlight{i}"]/div/div[1]/div[2]/div[2]/div/div/span/span[2]')))
			preco = preco.text
			preco = preco.replace('.','')
			preco = preco.replace(',','.')

			inserirTpPassagem(idPassagem[0],hSaida ,hChegada, duracao ,float(preco))
			i = menorI
		
		print(valor_final)
		idVoo +=1

	driver.close()

if __name__ == '__main___':
    main()  