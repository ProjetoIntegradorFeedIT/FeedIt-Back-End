# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
import hashlib
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao

# Router
router = APIRouter(
    prefix = "/login",
    tags = ["Login"],
    responses={404: {"description": "Not found"}},
)

# Função para descriptografar a senha que vem do banco de dados
def descriptografa_senha(stored_password, stored_salt, password_to_check):
    hash_to_check = hashlib.pbkdf2_hmac('sha256', password_to_check.encode('utf-8'), stored_salt, 100000)
    return hash_to_check == stored_password

# Depois remove o comentário
# O que fazer: Criar uma rota para autenticar um usuário
# Como? - Criar um endpoint POST /login que recebe um JSON com o email e a senha do usuário
# - O JSON deve conter os campos: email e senha
# - Se o email e a senha estiverem corretos, retornar um JSON com o status 200 e uma mensagem de sucesso
# - Se o email ou a senha estiverem incorretos, retornar um JSON com o status 401 e uma mensagem de erro
# Descomentar o Código a seguir
# @router.post("/")
# async def login(infos: InfosLogin):
#     session = Conexao().session
#     try:
#         # Aqui vem o seu código
#         return JSONResponse(content={"message": "Login realizado com sucesso!"})
#     except Exception as e:
#         return JSONResponse(content={"message": "Erro ao realizar o login!", "error": str(e)})
#     finally:
#         session.close()