from sqlalchemy import Column, String, Integer, UniqueConstraint

from model import Base


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column("pk_id_usuario", Integer, primary_key=True)
    nome = Column(String(200), unique=True)
    sobrenome = Column(String(200), unique=True)
    login = Column(String(200), unique=True)
    email = Column(String(200), unique=True)
    senha = Column(String(200), unique=True)
    nome_empresa = Column(String(200), unique=True)

    ## Criando um requisito de unicidade para garantir que não haja dois usuários com o mesmo login
    __table_args__ = (UniqueConstraint("login", name="login_unico"),)

    def __init__(self, nome:str, sobrenome:str, login:str, email:str, senha:str, nome_empresa:str):
        """
        Cria um Usuário com os dados fornecidos.

        Arguments:
            nome: Nome do usuário
            sobrenome: Sobrenome do usuário
            login: Login do usuário
            email: E-mail do usuário
            senha: Senha do usuário
            nome_empresa: Nome da empresa do usuário (ou nome de exibição do profissional)
        """
        self.nome = nome
        self.sobrenome = sobrenome
        self.login = login
        self.email = email
        self.senha = senha
        self.nome_empresa = nome_empresa