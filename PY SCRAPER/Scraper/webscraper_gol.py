from datetime import date
import datetime
from os import link
from pickle import FALSE, TRUE
import sys
import time
from tokenize import Double
from warnings import catch_warnings
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
	idVoo = 1
	for destinos in lista:
		driver.get(f'https://b2c.voegol.com.br/compra/busca-parceiros?pv=br&tipo=DF&de=GRU&para={destinos}&ida=01-12-2022&ADT=1&CHD=0&INF=0')
		#driver.maximize_window()
		time.sleep(15)
		indexMenor = 0
		indexMaior = 0
		maior = 0
		menor = 0

		vDiretos = []
		cards = driver.find_elements(By.XPATH ,'/html/body/app-root/b2c-flow/main/b2c-select-flight/div/section/form/div')
		for c in cards:
			tp_voo = c.find_element(By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[4]/a').get_attribute('innerHTML')
			if tp_voo.strip() == 'Direto':	
				try:		
					preco = WebDriverWait(c, 10).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[5]/span[3]'))).text
					preco = preco[2:]
					preco = preco.replace('.','')
					preco = preco.replace(',','.')
				except:
					preco = WebDriverWait(c, 10).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[5]/span[2]'))).text
					preco = preco[2:]
					preco = preco.replace('.','')
					preco = preco.replace(',','.')
				
				duracao =  WebDriverWait(c, 10).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[3]/span[2]'))).text
				hSaida =  WebDriverWait(c, 10).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[1]/span[2]'))).text
				hSaida = hSaida[6:]
				hChegada =  WebDriverWait(c, 10).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[2]/span[2]'))).text
				hChegada = hChegada[6:]
				v = [float(preco.strip()), hSaida, hChegada, duracao]
				vDiretos.append(v)
				maior =  vDiretos[0][0]
				menor =  vDiretos[0][0]
  
		if len(vDiretos) == 1:
			media = vDiretos[0][0]
			maior = media
			menor = media
			indexMenor = 0
			indexMaior = 0
   
		else:	
			for v in vDiretos:
				if v[0] <= menor:	
					menor = v[0]
					indexMenor = vDiretos.index(v)

				else:
					maior = v[0]
					indexMaior = vDiretos.index(v)

		if maior and menor !=0:
			media = (maior + menor)/2
		else:
			media = 0
			
		dataVoo = '2022-12-01'
		companhia = 'GOL'
		dataPesquisa = '2022-11-24'
		inserirPassagem(idVoo,companhia,media,dataVoo,str(dataPesquisa))	
		idPassagem = obterIdPassagem(idVoo, str(dataPesquisa),companhia)

		print('-------------\n' +
        	  f'{destinos}\n' +
           	  f'index menor = {indexMenor} - R${menor}\n' +
           	  f'index maior = {indexMaior} - R${maior}\n' +
           	  f'media = R${media}\n')	  

		inserirTpPassagem('MENOR',idPassagem,vDiretos[indexMenor][1], vDiretos[indexMenor][2], vDiretos[indexMenor][3], vDiretos[indexMenor][0])
		inserirTpPassagem('MAIOR',idPassagem,vDiretos[indexMaior][1], vDiretos[indexMaior][2], vDiretos[indexMaior][3], vDiretos[indexMaior][0])

		idVoo += 1

	driver.close()
 
if __name__ == '__main___':
    main()