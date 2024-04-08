from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.servico import Servico
from model.usuario import Usuario

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False, pool_size=20, max_overflow=20)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)

# Limpa a tabela 'usuario', caso existam dados, para inserir o conteúdo do arquivo 'usuario_db.sql'
with engine.connect() as connection:
    connection.execute(text("DELETE FROM usuarios"))
    connection.commit()

# Popula a tabela 'usuarios' com os dados do arquivo 'usuario_db.sql'
with open('database/usuario_db.sql') as f:
    data = f.read()

# Separa os comandos SQL no arquivo
statements = data.split(';')

# Executa os comandos SQL do arquivo
with engine.connect() as connection:
    for statement in statements:
        # Verifica e pula se existir um comando vazio
        if statement.strip():
            connection.execute(text(statement))
    # Faz o commit no banco
    connection.commit()
