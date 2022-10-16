# Vamos utilizar o pacote SQLAlchemy para acesso a banco de dados:
# https://docs.sqlalchemy.org
#
# Para isso, ele precisa ser instalado via pip (de preferência com o VS Code fechado):
# python -m pip install SQLAlchemy
#
# Além disso, o SQLAlchemy precisa de um driver do conexão ao banco. Isso depende do servidor
# (MySQL, Postgres, SQL Server, Oracle...) e do driver real. Vamos utilizar o driver MySQL-Connector,
# que também precisa ser inst   alado (de preferência com o VS Code fechado):
# python -m pip install mysql-connector-python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Como criar uma comunicação com o banco de dados:
# https://docs.sqlalchemy.org/en/14/core/engines.html
#
# Detalhes específicos ao MySQL
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqlconnector
#
# mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine('mysql+mysqlconnector://root:root@localhost/quando_eu_voo')

# A função text(), utilizada ao longo desse código, serve para encapsular um comando
# SQL qualquer, de modo que o SQLAlchemy possa entender!

def obterIdVssssssoo():
	# O with do Python é similar ao using do C#, ou o try with resources do Java.
	# Ele serve para limitar o escopo/vida do objeto automaticamente, garantindo
	# que recursos, como uma conexão com o banco, não sejam desperdiçados!
	with Session(engine) as sessao:
		pessoas = sessao.execute(text("SELECT id, nome, email FROM pessoa ORDER BY nome"))

		# Como cada registro retornado é uma tupla ordenada, é possível
		# utilizar a forma de enumeração de tuplas:
		for (id, nome, email) in pessoas:
			print(f'\nid: {id} / nome: {nome} / email: {email}')

		# Ou, se preferir, é possível retornar cada tupla, o que fica mais parecido
		# com outras linguagens de programação:
		#for pessoa in pessoas:
		#	print(f'\nid: {pessoa.id} / nome: {pessoa.nome} / email: {pessoa.email}')

def obterIdVoo(destino):
	with Session(engine) as sessao:
		parametro = {
			'destino': destino
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		idVoo = sessao.execute(text("SELECT idVoo FROM voo WHERE destino = :destino"), parametro).first()

		if idVoo == None:
			print('Voo não encontrado!')
		else:
			return idVoo

def obterIdVooGol(destinoSigla):
	with Session(engine) as sessao:
		parametro = {
			'destinoSigla': destinoSigla
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		idVoo = sessao.execute(text("SELECT idVoo FROM voo WHERE destinoSigla = :destinoSigla"), parametro).first()
		
		if idVoo == None:
			print('Voo não encontrado!')
		else:
			return idVoo[0]

def obterIdPassagem(idVoo, dataPesquisa):
	with Session(engine) as sessao:
		parametros = {
			'idVoo': idVoo,
			'dataPesquisa': dataPesquisa
		}

		# Mais informações sobre o método execute e sobre o resultado que ele retorna:
		# https://docs.sqlalchemy.org/en/14/orm/session_api.html#sqlalchemy.orm.Session.execute
		# https://docs.sqlalchemy.org/en/14/core/connections.html#sqlalchemy.engine.Result
		IdPassagem = sessao.execute(text("SELECT idPassagem FROM passagem WHERE idVoo = :idVoo AND dataPesquisa = :dataPesquisa"), parametros).first()

		if IdPassagem == None:
			print('Passagem não encontrada!')
		else:
			return IdPassagem[0]



def inserirVoo(origem, destino):
	# É importante utilizar o método begin() para que a sessão seja comitada
	# automaticamente ao final, caso não ocorra uma exceção!
	# Isso não foi necessário nos outros exemplos porque nenhum dado estava sendo
	# alterado lá! Caso alguma exceção ocorra, rollback() será executado automaticamente,
	# e nenhuma alteração será persistida. Para mais informações de como explicitar
	# esse processo de commit() e rollback():
	# https://docs.sqlalchemy.org/en/14/orm/session_basics.html#framing-out-a-begin-commit-rollback-block
	with Session(engine) as sessao, sessao.begin():
		voo = {
			'origem': origem,
			'destino': destino
		}

		sessao.execute(text("INSERT INTO voo (origem, destino) VALUES (:origem, :destino)"), voo)

		# Para inserir, ou atualizar, vários registros ao mesmo tempo, a forma mais rápida
		# é passar uma lista como segundo parâmetro:
		# lista = [ ... ]
		# sessao.execute(text("INSERT INTO pessoa (nome, email) VALUES (:nome, :email)"), lista)
  
def inserirPassagem(idVoo, companhia, media, dataVoo, dataPesquisa):
	with Session(engine) as sessao, sessao.begin():
		passagem = {
			'idVoo': idVoo,
			'companhia': companhia,
            'media': media,
            'dataVoo': dataVoo,
            'dataPesquisa': dataPesquisa
		}

		sessao.execute(text("INSERT INTO passagem (idVoo, companhia, media, dataVoo, dataPesquisa) VALUES (:idVoo, :companhia, :media, :dataVoo, :dataPesquisa)"), passagem)

def inserirTpPassagem(idPassagem, hSaida, hChegada, duracao, preco):
	with Session(engine) as sessao, sessao.begin():
		tpPassagem = {
			'idPassagem': idPassagem,
			'hSaida': hSaida,
            'hChegada': hChegada,
            'duracao': duracao,
            'preco': preco
		}

		sessao.execute(text("INSERT INTO tp_passagem (idPassagem, hSaida, hChegada, duracao, preco) VALUES (:idPassagem, :hSaida, :hChegada, :duracao, :preco)"), tpPassagem)


# O uso desse tipo de instrução é muito comum em Python!
# Quando executamos um arquivo direto pela linha de comando, como
# python exemplo_sql.py
# o Python fará com que a variável global __name__ valha '__main__', indicando
# que a execução do programa se deu a partir daquele arquivo, e não de outro.
# Quando o arquivo é importado, __name__ valerá o nome do arquivo sem a extensão
# .py, como 'exemplo_sql'
#if __name__ == '__main__':
#	listarPessoas()

# Para mais informações:
# https://docs.sqlalchemy.org/en/14/tutorial/dbapi_transactions.html
