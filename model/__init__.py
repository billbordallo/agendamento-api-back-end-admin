from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.servico import Servico

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

# Limpa a tabela 'servicos', caso existam dados, para inserir o conteúdo abaixo
with engine.connect() as connection:
    connection.execute(text("DELETE FROM servicos"))
    connection.commit()

# Popula a tabela 'servicos' com um serviços padrão (para fins de demonstração)
servico_sql = text('INSERT INTO servicos (pk_id_servico, nome_servico, duracao_servico, desc_servico, valor_servico) VALUES (:pk_id_servico, :nome_servico, :duracao_servico, :desc_servico, :valor_servico)')
servicos = [
    {
    "pk_id_servico": 1,
    "nome_servico": 'Corte de cabelo masculino',
    "duracao_servico": '40 minutos',
    "desc_servico": 'Corte de cabelo ao gosto do cliente',
    "valor_servico": 50,
    },
    {
    "pk_id_servico": 2,
    "nome_servico": 'Barba completa',
    "duracao_servico": '30 minutos',
    "desc_servico": 'Barba com relaxamento facial',
    "valor_servico": 40,
    },
    {
    "pk_id_servico": 3,
    "nome_servico": 'Cabelo e barba',
    "duracao_servico": '1 hora',
    "desc_servico": 'Corte de cabelo e barba na mesma sessão',
    "valor_servico": 80,
    }
]

# Executa os comandos SQL
with engine.connect() as connection:
    connection.execute(servico_sql, servicos)
    # Faz o commit no banco
    connection.commit()