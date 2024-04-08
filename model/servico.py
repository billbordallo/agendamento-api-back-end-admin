from sqlalchemy import Column, String, Integer, UniqueConstraint

from model import Base


class Servico(Base):
    __tablename__ = 'servicos'

    id = Column("pk_id_servico", Integer, primary_key=True)
    nome_servico = Column(String(200), unique=True)
    duracao_servico = Column(String(50), unique=False)
    desc_servico = Column(String(300), unique=False)
    valor_servico = Column(Integer, unique=False)

    # Criando um requisito de unicidade para garantir que não haja dois serviços com o mesmo nome
    __table_args__ = (UniqueConstraint("nome_servico", name="nome_servico_unico"),)

    def __init__(self, nome_servico:str, duracao_servico:str, desc_servico:str, valor_servico:int):
        """
        Cria um Serviço com os dados fornecidos.

        Arguments:
            nome_servico: Nome do serviço
            duracao_servico: Duração do serviço
            desc_servico: Descrição
            valor_servico: Valor (preço) do serviço
        """
        self.nome_servico = nome_servico
        self.duracao_servico = duracao_servico
        self.desc_servico = desc_servico
        self.valor_servico = valor_servico