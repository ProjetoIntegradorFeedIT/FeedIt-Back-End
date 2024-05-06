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
    prefix = "/img_recog",
    tags = ["Imagem_Reconhecimento"],
    responses={404: {"description": "Not found"}},
)

# Depois remove o comentário
# O que fazer: Criar uma rota para a verificação das imagens tiradas
# Como? - Criar um endpoint POST /verificar que recebe um JSON com a imagem tirada e o id da criança
# - O JSON deve conter os campos: imagem e id_crianca
# - Vamos utilizar o ChatGPT para verificar a imagem e retornar um JSON com o status 200 e uma mensagem de sucesso
# - Se ocorrer algum erro, retornar um JSON com o status 401 e uma mensagem de erro
@router.post("/verificar")
async def verificar_imagem(request: Request):
    session = Conexao().session
    try:
        # Aqui vem o seu código
        return JSONResponse(content={"message": "Imagem verificada com sucesso!"}) # Talvez seja necessário alterar o return
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao verificar a imagem!", "error": str(e)})
    finally:
        session.close()