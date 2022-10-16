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
from storage import *
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

def main(lista):
	cookie = False
 
	for destinos in lista:
		driver.get(f'https://b2c.voegol.com.br/compra/busca-parceiros?pv=br&tipo=DF&de=GRU&para={destinos}&ida=01-12-2022&ADT=1&CHD=0&INF=0')
		driver.maximize_window()
		time.sleep(7)
  
		# Verifica se há Cookie e aceita ele
		if cookie == False:
			cookiebtn = WebDriverWait(driver, 30).until(
				EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
			)
			cookie = True
			cookiebtn.click()
		
		# Iterar por div com o mesmo XPATH (Cards de voos)
		vDiretos = []
		cards = driver.find_elements(By.XPATH ,'/html/body/app-root/b2c-flow/main/b2c-select-flight/div/section/form/div')
		for c in cards:
			tp_voo = c.find_element(By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[4]/a').get_attribute('innerHTML')
			if tp_voo.strip() == 'Direto':
				preco = WebDriverWait(c, 20).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[5]/span[3]'))).text
				preco = preco[2:]
				preco = preco.replace('.','')
				preco = preco.replace(',','.')
				
				duracao =  WebDriverWait(c, 20).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[3]/span[2]'))).text
				hSaida =  WebDriverWait(c, 20).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[1]/span[2]'))).text
				hSaida = hSaida[6:]
				hChegada =  WebDriverWait(c, 20).until(EC.presence_of_element_located((By.XPATH ,'./div/div[1]/b2c-bar-product/div[2]/p[2]/span[2]'))).text
				hChegada = hChegada[6:]
				#print(duracao)
				#print(hSaida)
				#print(hChegada)
				print(preco.strip())
				v = [float(preco.strip()), hSaida, hChegada, duracao]
				vDiretos.append(v)
  
		if len(vDiretos) == 1:
			media = vDiretos[0][0]
			indexMenor = 0
			indexMaior = 0
			print(media)	
   
		else:
			menor = 100000000
			maior = 0
			for v in vDiretos:
				if v[0] < menor:	
					if menor > maior and menor != 100000000:
						maior = menor
      
					menor = v[0]
					indexMenor = vDiretos.index(v)
     
				elif v[0] > maior:
					if maior < menor and maior != 0:
						menor = maior
					maior = v[0]
					indexMaior = vDiretos.index(v)

			media = (maior + menor)/2
			print(media)
		
		idVoo = obterIdVooGol(destinos)
		dataVoo = '2022-12-01'
		companhia = 'GOL'
		dataPesquisa = datetime.datetime.now().date()
		inserirPassagem(idVoo,companhia,media,dataVoo,str(dataPesquisa))
  	
		idPassagem = obterIdPassagem(idVoo, str(dataPesquisa))

		print('-------------\n' +
        	  f'{destinos}\n' +
           	  f'index menor = {indexMenor}\n' +
           	  f'index maior = {indexMaior}\n' +
           	  f'media = {media}\n')

		inserirTpPassagem(idPassagem,vDiretos[indexMenor][1], vDiretos[indexMenor][2], vDiretos[indexMenor][3], vDiretos[indexMenor][0])
		inserirTpPassagem(idPassagem,vDiretos[indexMaior][1], vDiretos[indexMaior][2], vDiretos[indexMaior][3], vDiretos[indexMaior][0])

	driver.close()
 
if __name__ == '__main___':
    main()