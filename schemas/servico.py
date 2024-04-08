from pydantic import BaseModel
from typing import Optional, List
from model.servico import Servico


class ServicoSchema(BaseModel):
    """ Define como um novo serviço a ser inserido deve ser representado
    """
    id: Optional[int] = 1
    nome_servico: str = "Corte de cabelo"
    duracao_servico: str = "1 hora"
    desc_servico: str = "Corte de cabelo ao gosto do cliente"
    valor_servico: int = 50


class ServicoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do serviço.
    """
    id: int = 5

class ServicoBuscaNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do serviço.
    """
    nome_servico: str = "Corte de cabelo"

class ListagemServicoSchema(BaseModel):
    """ Define como uma listagem de serviços será retornada.
    """
    servicos:List[ServicoSchema]


def apresenta_servicos(servicos: List[Servico]):
    """ Retorna uma representação do serviço seguindo o schema definido em
        ServicoViewSchema.
    """
    result = []
    for servico in servicos:
        result.append({
            "id": servico.id,
            "nome_servico": servico.nome_servico,
            "duracao_servico": servico.duracao_servico,
            "desc_servico": servico.desc_servico,
            "valor_servico": servico.valor_servico,
        })

    return {"servicos": result}


class ServicoViewSchema(BaseModel):
    """ Define como um serviço será retornado.
    """
    id: int = 1
    nome_servico: str = "Corte de cabelo"
    duracao_servico: str = "1 hora"
    desc_servico: str = "Corte de cabelo ao gosto do cliente"
    valor_servico: str = 50


class ServicoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome_servico: str
    duracao_servico: str
    desc_servico: str
    valor_servico: str

def apresenta_servico(servico: Servico):
    """ Retorna uma representação do servico seguindo o schema definido em
        ServicoViewSchema.
    """
    return {
        "id": servico.id,
        "nome_servico": servico.nome_servico,
        "duracao_servico": servico.duracao_servico,
        "desc_servico": servico.desc_servico,
        "valor_servico": servico.valor_servico,
        }
