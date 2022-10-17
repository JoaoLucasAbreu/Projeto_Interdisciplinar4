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
 
	for destinos in lista:
		driver.get(f'https://www.latamairlines.com/br/pt/oferta-voos?origin=GRU&inbound=null&outbound=2022-12-01T15%3A00%3A00.000Z&destination={destinos}&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED')
		driver.maximize_window()
		time.sleep(10)
  
		# Verifica se há Cookie e aceita ele
		if cookie == False:
			cookiebtn = WebDriverWait(driver, 30).until(
				EC.presence_of_element_located((By.ID, "cookies-politics-button"))
			)
			cookie = True
			cookiebtn.click()
		
		# Iterar por div com o mesmo XPATH (Cards de voos)
		vDiretos = []
		cards = driver.find_elements(By.XPATH ,'/html/body/div[1]/div/main/div/div/div[1]/ol[2]/li')
		for c in cards:
			tp_voo = c.find_element(By.XPATH ,'./div/div/div[2]/div[1]/a/span').get_attribute('innerHTML')
			if tp_voo.strip() == 'Direto':

				preco = WebDriverWait(c, 20).until(EC.presence_of_element_located((By.XPATH ,'./div/div/div[2]/div[2]/div/div/div/span/span[2]'))).get_attribute('innerHTML')
				preco = preco.replace('.','')
				preco = preco.replace(',','.')
				
				duracao =  WebDriverWait(c, 20).until(EC.presence_of_element_located((By.XPATH ,'./div/div/div[1]/div[2]/div[1]/div[2]/span[2]'))).get_attribute('innerHTML')
				h1 = duracao[0:2].strip()
				h2 = duracao[-7:-5].replace(" ", "0")
				if len(h1) == 1:
					h1 = '0' + h1
				duracao = h1 +':' + h2

				hSaida =  WebDriverWait(c, 20).until(EC.presence_of_element_located((By.XPATH ,'./div/div/div[1]/div[2]/div[1]/div[1]/span[1]'))).text
				hChegada =  WebDriverWait(c, 20).until(EC.presence_of_element_located((By.XPATH ,'./div/div/div[1]/div[2]/div[1]/div[3]/span[1]'))).text
				if "+" in hChegada or "\n" in hChegada:
					hChegada = hChegada[:-2]
     
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
			maior = 0
			menor = 999999999
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
		
		#idVoo = obterIdVooGol(destinos)
		dataVoo = '2022-12-01'
		companhia = 'LATAM'
		dataPesquisa = datetime.datetime.now().date()
		if media > 10000:
			print('PAROU')
		#inserirPassagem(idVoo,companhia,media,dataVoo,str(dataPesquisa))
  	
		#idPassagem = obterIdPassagem(idVoo, str(dataPesquisa))

		print('-------------\n' +
        	  f'{destinos}\n' +
           	  f'index menor = {indexMenor}\n' +
           	  f'index maior = {indexMaior}\n' +
           	  f'media = {media}\n')

		#inserirTpPassagem('MENOR',idPassagem,vDiretos[indexMenor][1], vDiretos[indexMenor][2], vDiretos[indexMenor][3], vDiretos[indexMenor][0])
		#inserirTpPassagem('MAIOR',idPassagem,vDiretos[indexMaior][1], vDiretos[indexMaior][2], vDiretos[indexMaior][3], vDiretos[indexMaior][0])

	driver.close()
 
if __name__ == '__main___':
    main()