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
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

driver = webdriver.Chrome()
driver.get('https://google.com')

input = WebDriverWait(driver, 20).until(
	EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="q"]'))
)

input.send_keys('Montanha')
input.send_keys(Keys.RETURN)

link_imagens = WebDriverWait(driver, 20).until(
	EC.element_to_be_clickable((By.XPATH, "//a[text()='Imagens']"))
)
link_imagens.click()

imagens = WebDriverWait(driver, 20).until(
	EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'img.rg_i'))
)

dados = []

for imagem in imagens:
	dados.append({
		'descr': imagem.get_attribute('alt'),
		'largura': int(imagem.get_attribute('width')),
		'altura': int(imagem.get_attribute('height'))
	})

print(dados)

driver.close()
