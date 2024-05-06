# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao

# Router
router = APIRouter(
    prefix = "/responsavel",
    tags = ["Responsavel"],
    responses={404: {"description": "Not found"}},
)

# As funções devem conectar no bd para conseguir suas informações necessarias
# Deve se retornar oq for necessário para a tela

# Esta função deve retornar uma lista das criancas vinculadas ao responsável
# Cada criança deve ter os seguintes campos: id_crianca, nome_crianca, e suas respectivas missões
@router.get("/listar_criancas/{id_responsavel}")
async def listar_criancas(id_responsavel: int):
    session = Conexao().session
    try:
        # Aqui vem o codigo
        return "Coloque o retorno aqui"
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