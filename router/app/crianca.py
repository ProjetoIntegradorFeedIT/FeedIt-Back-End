# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao, Crianca, Pet

# Router
router = APIRouter(
    prefix = "/crianca",
    tags = ["Crianca"],
    responses={404: {"description": "Not found"}},
)

# Listar todas as personalizações
@router.get("/listar_personalizacao")
async def listar_personalizacao():
    session = Conexao().session
    try:
        personalizacoes = session.query(Personalizacao).all()
        return personalizacoes
    finally:
        session.close()

# Atualizar personalização do Pet
@router.post("/salvar_personalizacao_pet")
async def salvar_personalizacao(request: Request):
    session = Conexao().session
    try:
        data = await request.json()

        update_pet = session.query(Pet).filter(Pet.id_pet == data['id_pet']).first()
        update_pet.cor = data["cor"]
        update_pet.chapeu = data["chapeu"]
        update_pet.roupa = data['roupa']
        update_pet.fundo = data["fundo"]

        session.commit()
        return JSONResponse(content={"message": "Personalização do Pet alterada!"})
    finally:
        session.close()

# Mostra os status do Pet
@router.get("/mostrar_status/{id_pet}")
async def mostrar_status(id_pet: int):
    session = Conexao().session
    try:
        pet = session.query(Pet).filter(Pet.id_pet == 1).all()
        pet = pet[0]
        # Converter o objeto Pet em um dicionário
        pet_dict = {
            "id_pet": pet.id_pet,
            "alimentacao": pet.alimentacao,
            "energia": pet.energia,
            "felicidade": pet.felicidade,
            "forca": pet.forca
        }
        return JSONResponse(content={"message": "Status do Pet encontrado.", "pet": pet_dict})
    finally:
        session.close()

# Pega as missões do Pet da Criança