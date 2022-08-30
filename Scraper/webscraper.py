# Vamos utilizar o pacote Selenium Python para manipular browsers via código:
# https://selenium-python.readthedocs.io/
#
# Para isso, ele precisa ser instalado via pip (de preferência com o VS Code fechado):
# python -m pip install selenium
#
# Depois de instalar o Selenium Python, é necessário instalar o driver referente
# ao browser que será utilizado:
#
# Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
# Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# Firefox: https://github.com/mozilla/geckodriver/releases
# Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/
#
# Depois de baixar o driver, garantir que ele seja instalado/descompactado em uma
# pasta que pertença ao PATH global do sistema (de preferência com o VS Code fechado).
#
# No Linux, podem ser as pastas /usr/bin, /usr/local/bin ou outra que esteja no PATH.
# Para adicionar outra pasta ao PATH, basta editar o arquivo ~/.bashrc, e adicionar
# uma linha parecida com essa:
# export PATH=/nova/pasta/para/adicionar:${PATH}
#
# No Windows, o PATH pode ser editado clicando com o botão direito sobre o ícone do
# Computador (no Windows Explorer), depois no menu "Propriedades", em seguida "Configurações
# avançadas do sistema" e, por fim, em "Variáveis de Ambiente".
from os import link
import sys
import time
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
driver.get('https://www.latamairlines.com/br/pt/oferta-voos?origin=GRU&inbound=null&outbound=2022-12-01T15%3A00%3A00.000Z&destination=SSA&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED')

# Cookie
cookiebtn = WebDriverWait(driver, 10).until(
	EC.presence_of_element_located((By.ID, "cookies-politics-button"))
)

cookiebtn.click()

# Tela 1
# Origem
origem = WebDriverWait(driver, 20).until(
	EC.presence_of_element_located((By.ID, "undefined-dialog-open"))
)

origem.send_keys('São Paulo, GRU - Brasil')
origem.send_keys(Keys.RETURN)



input = WebDriverWait(driver, 20).until(
	EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="q"]'))
)

input.send_keys('Montanha')
input.send_keys(Keys.RETURN)

link_imagens = WebDriverWait(driver, 20).until(
	EC.element_to_be_clickable((By.XPATH, "//a[text()='Imagens']"))
)
link_imagens.click()

voos = WebDriverWait(driver, 20).until(
	EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.rg_i'))
)

dados = []

""" for v in voos:
	dados.append({
		'destino': imagem.get_attribute('alt'),
		'hsaida': int(imagem.get_attribute('width')),
		'hchegada': int(imagem.get_attribute('height')),
		'duracao':,
		'valor':
	}) """

print(dados)

driver.close()
