# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao, Crianca, Pet, CriancaMissao, Missao

# Router
router = APIRouter(
    prefix = "/crianca",
    tags = ["Crianca"],
    responses={404: {"description": "Not found"}},
)

#Infos da criança
@router.get("/info_crianca/{id_crianca}")
async def info_crianca(id_crianca: int):
    session = Conexao().session
    try:
        crianca = session.query(Crianca).filter(Crianca.id_crianca == id_crianca).first()
        pet = session.query(Pet).filter(Pet.id_crianca == crianca.id_crianca).first()
        dict_crianca = {
            "id_crianca": crianca.id_crianca,
            "nome_crianca": crianca.nome_crianca,
            "nivel": crianca.nivel,
            "xp_atual": crianca.xp_atual,
            "xp_necessario": crianca.xp_necessario,
            "moedas": crianca.dinheiro,
            "id_pet": pet.id_pet,
            "nome_pet": pet.nome_pet,
            "tipo_pet": pet.tipo_pet,
            "cor": pet.cor,
            "chapeu": pet.chapeu,
            "roupa": pet.roupa,
            "fundo": pet.fundo,
        }
        return JSONResponse(content={"message": "Criança encontrada.", "crianca": dict_crianca})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao encontrar a criança!", "error": str(e)})
    finally:
        session.close()

# Listar todas as personalizações
@router.get("/listar_personalizacao")
async def listar_personalizacao():
    session = Conexao().session
    try:
        personalizacoes = session.query(Personalizacao).all()
        return personalizacoes
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao listar personalizações!", "error": str(e)})
    finally:
        session.close()

# Listar todas as personalizações divididas por tipo
@router.get("/listar_personalizacao_tipo/{tipo_pet}")
async def listar_personalizacao_tipo(tipo_pet: str):
    session = Conexao().session
    try:
        personalizacoes = session.query(Personalizacao).filter(Personalizacao.tipo_perso == tipo_pet).all()
        dict_personalizacoes = {
            "chapeu": [],
            "roupa": [],
            "fundo": [],
            "cor": []
        }
        for p in personalizacoes:
            if p.tipo_perso == "Chapeu":
                dict_personalizacoes["chapeu"].append({
                    "id_perso": p.id_perso,
                    "nome_perso": p.nome_perso,
                    "url": p.url_img,
                    "tipo": p.tipo_perso,
                    "valor": p.preco
                })
            elif p.tipo_perso == "Roupa":
                dict_personalizacoes["roupa"].append({
                    "id_perso": p.id_perso,
                    "nome_perso": p.nome_perso,
                    "url": p.url_img,
                    "tipo": p.tipo_perso,
                    "valor": p.preco
                })
            elif p.tipo_perso == "Fundo":
                dict_personalizacoes["fundo"].append({
                    "id_perso": p.id_perso,
                    "nome_perso": p.nome_perso,
                    "url": p.url_img,
                    "tipo": p.tipo_perso,
                    "valor": p.preco
                })
            elif p.tipo_perso == "Cor":
                dict_personalizacoes["cor"].append({
                    "id_perso": p.id_perso,
                    "nome_perso": p.nome_perso,
                    "url": p.url_img,
                    "tipo": p.tipo_perso,
                    "valor": p.preco
                })
        return dict_personalizacoes
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao listar personalizações!", "error": str(e)})
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
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao alterar a personalização do Pet!", "error": str(e)})
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
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao encontrar o status do Pet!", "error": str(e)})
    finally:
        session.close()

# Pega as missões do Pet da Criança
@router.get("/missao_pet/{id_crianca}")
async def missao_pet(id_crianca: int):
    session = Conexao().session
    try:
        missao = session.query(CriancaMissao).filter(CriancaMissao.id_crianca == id_crianca).all()
        dict_missao = {}
        for m in missao:
            select = session.query(Missao).filter(Missao.id_missao == m.id_missao).first()
            dict_missao[select.nome_missao] = {
                "tipo_missao": select.tipo_missao,
                "nome_missao": select.nome_missao,
                "valor": select.valor,
                "tamanho": select.tamanho,
                "progresso_tarefa": m.progresso_tarefa,
            }
        return dict_missao
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao encontrar as missões do Pet!", "error": str(e)})
    finally:
        session.close()
