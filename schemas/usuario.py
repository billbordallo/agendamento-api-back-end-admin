from pydantic import BaseModel
from typing import Optional, List
from model.usuario import Usuario


class UsuarioSchema(BaseModel):
    """ Define como um novo usuário a ser inserido deve ser representado
    """
    id: Optional[int] = 1
    nome: str = "José"
    sobrenome: str = "da Silva"
    login: str = "jose.silva"
    email: str = "jose@email.com"
    senha: str = "1234"
    nome_empresa: str = "Barbearia do José"


class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do usuário.
    """
    id: int = 5

class UsuarioBuscaNomeSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do usuário.
    """
    nome: str = "José"

class ListagemUsuarioSchema(BaseModel):
    """ Define como uma listagem de usuários será retornada.
    """
    usuarios:List[UsuarioSchema]


def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "sobrenome": usuario.sobrenome,
            "login": usuario.login,
            "email": usuario.email,
            "senha": usuario.senha,
            "nome_empresa": usuario.nome_empresa,
        })

    return {"usuarios": result}


class UsuarioViewSchema(BaseModel):
    """ Define como um usuário será retornado.
    """
    id: int = 1
    nome: str = "José"
    sobrenome: str = "da Silva"
    login: str = "jose.silva"
    email: str = "jose@email.com"
    senha: str = "1234"
    nome_empresa: str = "Barbearia do José"


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str
    sobrenome: str
    login: str
    email: str
    nome_empresa: str

def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do usuario seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "sobrenome": usuario.sobrenome,
        "login": usuario.login,
        "email": usuario.email,
        "nome_empresa": usuario.nome_empresa,
        }
