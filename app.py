from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request, jsonify, abort
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.exc import IntegrityError

from model import Session, Servico
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="API de agendamento (microsserviço de usuários e serviços prestados)", version="1.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
servicos_tag = Tag(name="Serviços", description="Adição, visualização e remoção de serviços da base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/servico', tags=[servicos_tag],
          responses={"200": ServicoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_servico(form: ServicoSchema):
    """Adiciona um novo Serviço à base de dados

    Retorna uma representação do serviço.
    """
    print(form)
    servico_criado = Servico(
        nome_servico=form.nome_servico,
        duracao_servico=form.duracao_servico,
        desc_servico=form.desc_servico,
        valor_servico=form.valor_servico,
    )
    
    logger.info(f"Adicionando agendamento: '{servico_criado.nome_servico}', '{servico_criado.duracao_servico}', '{servico_criado.desc_servico}', '{servico_criado.valor_servico}'")
    try:
        # criando conexão com a base
        session = Session()

        # adicionando agendamento
        session.add(servico_criado)
        # efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.info("Serviço adicionado: %s" % servico_criado)
        return apresenta_servico(servico_criado), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Não foi possível adicionar o serviço, pois já existe um com o mesmo nome na base :/"
        logger.warning(f"Erro ao adicionar serviço, já existe um com o mesmo nome na base '{servico_criado.nome_servico}', {error_msg}, {e}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível inserir o serviço :/"
        logger.warning(f"Erro ao adicionar o serviço '{servico_criado.nome_servico}', {error_msg}, {e}")
        return {"message": error_msg}, 400
    finally:
        session.close()


@app.get('/servicos', tags=[servicos_tag],
         responses={"200": ListagemServicoSchema, "404": ErrorSchema})
def get_servicos():
    """Faz a busca por todos os Servicos existentes

    Retorna uma representação da listagem de servicos.
    """
    logger.debug(f"Coletando servicos ")
    # criando conexão com a base
    session = Session()
    try:
        # fazendo a busca
        servicos = session.query(Servico).all()

        if not servicos:
            # se não há servicos cadastrados
            msg = "Não há servicos cadastrados :/"
            return {"message": msg}, 200
        else:
            logger.debug(f"%d servicos econtrados" % len(servicos))
            # retorna a representação de agendamento
            print(servicos)
            return apresenta_servicos(servicos), 200
    finally:    
        session.close()

@app.delete('/servico', tags=[servicos_tag],
            responses={"200": ServicoDelSchema, "404": ErrorSchema})
def del_servico(query: ServicoBuscaSchema):
    """Deleta um Servico a partir do id do servico

    Retorna uma mensagem de confirmação da remoção.
    """
    servico_id = query.id
    print(servico_id)
    logger.debug(f"Deletando dados sobre servico #{servico_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Servico).filter(Servico.id == servico_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletando servico #{servico_id}")
        return {"mesage": "Servico removido", "id": servico_id}, 200
    else:
        # se o servico não foi encontrado
        error_msg = "Servico não encontrado na base :/"
        logger.warning(f"Erro ao deletar servico #'{servico_id}', {error_msg}")
        return {"mesage": error_msg}, 404