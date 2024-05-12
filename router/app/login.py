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

# Função para criptografar a senha
def criptografar_senha(senha):
    # Codificando a senha em bytes
    senha_bytes = senha.encode('utf-8')

    # Criando um objeto de hash usando o algoritmo SHA-256
    sha256 = hashlib.sha256()

    # Atualizando o objeto de hash com a senha codificada
    sha256.update(senha_bytes)

    # Gerando o hash da senha e retornando como hexadecimal
    senha_hash = sha256.hexdigest()
    
    return senha_hash

# Função para descriptografar a senha que vem do banco de dados
def verificar_senha(senha, senha_hash):
    # Criptografando a senha fornecida
    senha_fornecida_hash = criptografar_senha(senha)

    # Verificando se a senha fornecida e a senha armazenada são iguais
    if senha_fornecida_hash == senha_hash:
        return True
    else:
        return False
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