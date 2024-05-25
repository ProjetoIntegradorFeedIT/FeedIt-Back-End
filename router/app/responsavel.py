# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao, UsuarioCrianca, Crianca, CriancaMissao, Missao

# Router
router = APIRouter(
    prefix = "/responsavel",
    tags = ["Responsavel"],
    responses={404: {"description": "Not found"}},
)

# Função quick_sort
def quick_sort(lista):
    if len(lista) <= 1:
        return lista
    else:
        pivot = lista[len(lista) // 2]
        esq = [x for x in lista if x < pivot]
        meio = [x for x in lista if x == pivot]
        dir = [x for x in lista if x > pivot]
        return quick_sort(esq) + meio + quick_sort(dir)


# As funções devem conectar no bd para conseguir suas informações necessarias
# Deve se retornar oq for necessário para a tela

# Esta função deve retornar uma lista das criancas vinculadas ao responsável
# Cada criança deve ter os seguintes campos: id_crianca, nome_crianca, e suas respectivas missões
@router.get("/listar_criancas/{id_responsavel}")
async def listar_criancas(id_responsavel: int):
    session = Conexao().session
    try:
        # criancas = session.query(UsuarioCrianca).filter(UsuarioCrianca.id_user == id_responsavel).all()
        id_criancas = [result[0] for result in session.query(UsuarioCrianca.id_crianca).filter(UsuarioCrianca.id_user == id_responsavel).all()]

        if not id_criancas:
            raise HTTPException(status_code=204, detail="Crianças não encontradas para este responsável")
        
        criancas = {}
        for id in id_criancas:
            crianca = session.query(Crianca).filter(Crianca.id_crianca == id).first()
            criancas[crianca.nome_crianca] = crianca
            missoes = session.query(CriancaMissao).filter(CriancaMissao.id_crianca == crianca.id_crianca).all()
            dict_missao = {}
            for m in missoes:
                select = session.query(Missao).filter(Missao.id_missao == m.id_missao).first()
                dict_missao[select.nome_missao] = {
                    "tipo_missao": select.tipo_missao,
                    "nome_missao": select.nome_missao,
                    "valor": select.valor,
                    "tamanho": select.tamanho,
                    "progresso_tarefa": m.progresso_tarefa,
                }
            criancas[crianca.nome_crianca].missao = dict_missao
            
        # return JSONResponse(content={"criancas": criancas}, status_code=200)
        return criancas
    
    except Exception as e:
        # Logar o erro pode ser útil para depuração
        print(f"Erro ao listar crianças: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
    finally:
        session.close()

# Esta função deve aumentar o progresso de uma missão de uma criança
# Descomentar o Código a seguir
# @router.post("/aumentar_missao")
# async def aumentar_missao(missao: Missao):
#     session = Conexao().session
#     try:
#         # Aqui vem o codigo
#         return "Coloque o retorno aqui"
#     finally:
#         session.close()

# Esta função deve diminuir o progresso de uma missão de uma criança
# Descomentar o Código a seguir
# @router.post("/diminuir_missao")
# async def diminuir_missao(missao: Missao):
#     session = Conexao().session
#     try:
#         # Aqui vem o codigo
#         return "Coloque o retorno aqui"
#     finally:
#         session.close()

# Esta função deve retornar a tela da criança
@router.get("/ir_para_tela_crianca/{id_crianca}")
async def ir_para_tela_crianca(id_crianca: int):
    session = Conexao().session
    try:
        # Aqui vem o codigo
        return "Coloque o retorno aqui"
    finally:
        session.close()