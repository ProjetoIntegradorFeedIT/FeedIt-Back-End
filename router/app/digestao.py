# Imports
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import requests
import os
import re
from openai import OpenAI

# import db connection
from database.conexao import Conexao
from database.sqlalchemy import PetGrupoAlimento, Pet, GrupoAlimentos, Crianca

# Router
router = APIRouter(
    prefix="/digestao",
    tags=["Digestao"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def digestao(request: Request):
    session = Conexao().session
    try:
        data = await request.json()

        select_pet = session.query(Pet).filter(Pet.id_pet == data['id_pet']).first()
        select_estomago = session.query(PetGrupoAlimento).filter(PetGrupoAlimento.id_pet == data['id_pet']).all()
        for alimento in select_estomago:
            select_grupo = session.query(GrupoAlimentos).filter(GrupoAlimentos.id == alimento.id_grupo).first()
            diferenca = datetime.now() - alimento.consumo
            if select_grupo.grupo == 'Frutas':
                if diferenca > timedelta(minutes=45):
                    alimento.digeriu = 1
                    session.commit()
                    if select_pet.energia - select_grupo.energia < 0:
                        select_pet.energia = 0
                    else:
                        select_pet.energia -= select_grupo.energia
                    if select_pet.alimentacao - select_grupo.alimentacao < 0:
                        select_pet.alimentacao = 0
                    else:
                        select_pet.alimentacao -= select_grupo.alimentacao
                    if select_pet.felicidade - select_grupo.felicidade < 0:
                        select_pet.felicidade = 0
                    else:
                        select_pet.felicidade -= select_grupo.felicidade
                    if select_pet.forca - select_grupo.forca < 0:
                        select_pet.forca = 0
                    else:
                        select_pet.forca -= select_grupo.forca
                    session.commit()
            elif select_grupo.grupo == 'Vegetais e folhas':
                if diferenca > timedelta(minutes=90):
                    alimento.digeriu = 1
                    session.commit()
                    if select_pet.energia - select_grupo.energia < 0:
                        select_pet.energia = 0
                    else:
                        select_pet.energia -= select_grupo.energia
                    if select_pet.alimentacao - select_grupo.alimentacao < 0:
                        select_pet.alimentacao = 0
                    else:
                        select_pet.alimentacao -= select_grupo.alimentacao
                    if select_pet.felicidade - select_grupo.felicidade < 0:
                        select_pet.felicidade = 0
                    else:
                        select_pet.felicidade -= select_grupo.felicidade
                    if select_pet.forca - select_grupo.forca < 0:
                        select_pet.forca = 0
                    else:
                        select_pet.forca -= select_grupo.forca
                    session.commit()
            elif select_grupo.grupo == 'Carne e ovos':
                if diferenca > timedelta(minutes=210):
                    alimento.digeriu = 1
                    session.commit()
                    if select_pet.energia - select_grupo.energia < 0:
                        select_pet.energia = 0
                    else:
                        select_pet.energia -= select_grupo.energia
                    if select_pet.alimentacao - select_grupo.alimentacao < 0:
                        select_pet.alimentacao = 0
                    else:
                        select_pet.alimentacao -= select_grupo.alimentacao
                    if select_pet.felicidade - select_grupo.felicidade < 0:
                        select_pet.felicidade = 0
                    else:
                        select_pet.felicidade -= select_grupo.felicidade
                    if select_pet.forca - select_grupo.forca < 0:
                        select_pet.forca = 0
                    else:
                        select_pet.forca -= select_grupo.forca
                    session.commit()
            elif select_grupo.grupo == 'Cereais, tubérculos, pão e raízes':
                if diferenca > timedelta(minutes=150):
                    alimento.digeriu = 1
                    session.commit()
                    if select_pet.energia - select_grupo.energia < 0:
                        select_pet.energia = 0
                    else:
                        select_pet.energia -= select_grupo.energia
                    if select_pet.alimentacao - select_grupo.alimentacao < 0:
                        select_pet.alimentacao = 0
                    else:
                        select_pet.alimentacao -= select_grupo.alimentacao
                    if select_pet.felicidade - select_grupo.felicidade < 0:
                        select_pet.felicidade = 0
                    else:
                        select_pet.felicidade -= select_grupo.felicidade
                    if select_pet.forca - select_grupo.forca < 0:
                        select_pet.forca = 0
                    else:
                        select_pet.forca -= select_grupo.forca
                    session.commit()
            elif select_grupo.grupo == 'Legumes':
                if diferenca > timedelta(minutes=90):
                    alimento.digeriu = 1
                    session.commit()
                    if select_pet.energia - select_grupo.energia < 0:
                        select_pet.energia = 0
                    else:
                        select_pet.energia -= select_grupo.energia
                    if select_pet.alimentacao - select_grupo.alimentacao < 0:
                        select_pet.alimentacao = 0
                    else:
                        select_pet.alimentacao -= select_grupo.alimentacao
                    if select_pet.felicidade - select_grupo.felicidade < 0:
                        select_pet.felicidade = 0
                    else:
                        select_pet.felicidade -= select_grupo.felicidade
                    if select_pet.forca - select_grupo.forca < 0:
                        select_pet.forca = 0
                    else:
                        select_pet.forca -= select_grupo.forca
                    session.commit()
            elif select_grupo.grupo == 'Fungos':
                if diferenca > timedelta(minutes=90):
                    alimento.digeriu = 1
                    session.commit()
                    if select_pet.energia - select_grupo.energia < 0:
                        select_pet.energia = 0
                    else:
                        select_pet.energia -= select_grupo.energia
                    if select_pet.alimentacao - select_grupo.alimentacao < 0:
                        select_pet.alimentacao = 0
                    else:
                        select_pet.alimentacao -= select_grupo.alimentacao
                    if select_pet.felicidade - select_grupo.felicidade < 0:
                        select_pet.felicidade = 0
                    else:
                        select_pet.felicidade -= select_grupo.felicidade
                    if select_pet.forca - select_grupo.forca < 0:
                        select_pet.forca = 0
                    else:
                        select_pet.forca -= select_grupo.forca
                    session.commit()
            elif select_grupo.grupo == 'Leite e laticínios':
                if diferenca > timedelta(minutes=150):
                    alimento.digeriu = 1
                    session.commit()
                    if select_pet.energia - select_grupo.energia < 0:
                        select_pet.energia = 0
                    else:
                        select_pet.energia -= select_grupo.energia
                    if select_pet.alimentacao - select_grupo.alimentacao < 0:
                        select_pet.alimentacao = 0
                    else:
                        select_pet.alimentacao -= select_grupo.alimentacao
                    if select_pet.felicidade - select_grupo.felicidade < 0:
                        select_pet.felicidade = 0
                    else:
                        select_pet.felicidade -= select_grupo.felicidade
                    if select_pet.forca - select_grupo.forca < 0:
                        select_pet.forca = 0
                    else:
                        select_pet.forca -= select_grupo.forca
                    session.commit()
            elif select_grupo.grupo == 'Doces, Petiscos':
                if diferenca > timedelta(minutes=45):
                    alimento.digeriu = 1
                    session.commit()
                    if select_pet.energia - select_grupo.energia < 0:
                        select_pet.energia = 0
                    else:
                        select_pet.energia -= select_grupo.energia
                    if select_pet.alimentacao - select_grupo.alimentacao < 0:
                        select_pet.alimentacao = 0
                    else:
                        select_pet.alimentacao -= select_grupo.alimentacao
                    if select_pet.felicidade - select_grupo.felicidade < 0:
                        select_pet.felicidade = 0
                    else:
                        select_pet.felicidade -= select_grupo.felicidade
                    if select_pet.forca - select_grupo.forca < 0:
                        select_pet.forca = 0
                    else:
                        select_pet.forca -= select_grupo.forca
                    session.commit()

        select_posDigestao = session.query(Pet).filter(Pet.id_pet == data['id_pet']).first()

        return JSONResponse(content={"message": "Digestão realizada!", "alimentacao": select_posDigestao.alimentacao, "energia": select_posDigestao.energia, "felicidade": select_posDigestao.felicidade, "forca": select_posDigestao.forca})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao digerir!", "error": str(e), "status_code": 500})
    finally:
        session.close()