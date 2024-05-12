# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
import hashlib
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Usuario

# Router
router = APIRouter(
    prefix = "/cadastro",
    tags = ["Cadastro"],
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

# Depois remove o comentário
# O que fazer: Criar uma rota para cadastrar um novo usuário
# Como? - Criar um endpoint POST /cadastrar que recebe um JSON com os dados do usuário e salva no banco de dados
# - O JSON deve conter os campos: nome, email, senha, cpf ou crm, e tipo (responsavel ou médico)
# - Se o usuário for um responsável, salvar o nome, email, senha e cpf no banco de dados
# - Se o usuário for um médico, salvar o nome, email, senha e crm no banco de dados
# - Retornar um JSON com o status 200 e uma mensagem de sucesso
# - Se ocorrer algum erro, retornar um JSON com o status 401 e uma mensagem de erro
# - Se o usuário já existir, retornar um JSON com o status 401 e uma mensagem de erro - Verificar se o email já está cadastrado no banco de dados

@router.post("/responsavel")
async def cadastrar_usuario_responsavel(request: Request):
    session = Conexao().session
    try:
        data = await request.json()
        # Aqui vem o seu código
        return JSONResponse(content={"message": "Usuário cadastrado com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao cadastrar o usuário!", "error": str(e)})
    finally:
        session.close()

# Neste caso os dados do médico nos serão enviados por email, com a senha já criptografada e o salt, não podemos ter acesso a ela, apenas verificaremos o crm e etão cadastraremos o médico
@router.post("/profissional")
async def cadastrar_usuario_profissional(request: Request):
    session = Conexao().session
    try:
        # Aqui vem o seu código
        return JSONResponse(content={"message": "Usuário cadastrado com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao cadastrar o usuário!", "error": str(e)})
    finally:
        session.close()

# Neste caso a crinca só precisa dos campos nome e senha
@router.post("/crianca")
async def cadastrar_usuario_crianca(request: Request):
    session = Conexao().session
    try:
        # Aqui vem o seu código
        return JSONResponse(content={"message": "Usuário cadastrado com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao cadastrar o usuário!", "error": str(e)})
    finally:
        session.close()