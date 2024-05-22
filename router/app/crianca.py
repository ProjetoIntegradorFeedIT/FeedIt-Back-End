# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao, Crianca, Pet, CriancaMissao, Missao, PersonalizacaoPet

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
        if not crianca:
            raise HTTPException(status_code=404, detail="Criança não encontrada")

        pet = session.query(Pet).filter(Pet.id_crianca == crianca.id_crianca).first()
        if not pet:
            raise HTTPException(status_code=404, detail="Pet não encontrado")

        get_cor = session.query(Personalizacao).filter(Personalizacao.id_perso == pet.cor).first()
        get_chapeu = session.query(Personalizacao).filter(Personalizacao.id_perso == pet.chapeu).first()
        get_roupa = session.query(Personalizacao).filter(Personalizacao.id_perso == pet.roupa).first()
        get_fundo = session.query(Personalizacao).filter(Personalizacao.id_perso == pet.fundo).first()

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
            "cor": get_cor.url_img if get_cor else None,
            "chapeu": get_chapeu.url_img if get_chapeu else None,
            "roupa": get_roupa.url_img if get_roupa else None,
            "fundo": get_fundo.url_img if get_fundo else None,
        }
        return JSONResponse(content={"message": "Criança encontrada.", "crianca": dict_crianca})
    except HTTPException as e:
        return JSONResponse(content={"message": e.detail}, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao encontrar a criança!", "error": str(e)}, status_code=500)
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
        personalizacoes = session.query(Personalizacao).filter(Personalizacao.tipo_pet == tipo_pet).all()
        dict_personalizacoes = {}
        for p in personalizacoes:
            if p.tipo_perso not in dict_personalizacoes:
                dict_personalizacoes[p.tipo_perso] = []
            dict_personalizacoes[p.tipo_perso].append({
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

# Personalização do pet + lista de personalizações + desbloqueio ou não
@router.get("/personalizacao_pet/{id_crianca}")
async def personalizacao_pet(id_crianca: int):
    session = Conexao().session
    try:
        crianca = session.query(Crianca).filter(Crianca.id_crianca == id_crianca).first()
        if not crianca:
            raise HTTPException(status_code=404, detail="Criança não encontrada")

        pet = session.query(Pet).filter(Pet.id_crianca == crianca.id_crianca).first()
        if not pet:
            raise HTTPException(status_code=404, detail="Pet não encontrado")
        
        personalizacoes = session.query(Personalizacao).filter(Personalizacao.tipo_pet == pet.tipo_pet).all()
        # personalizacoesPet = session.query(PersonalizacaoPet).filter(PersonalizacaoPet.id_pet == pet.id_pet).all()

        dict_personalizacoes = {}
        for p in personalizacoes:

            personalizacao_pet = session.query(PersonalizacaoPet).filter(PersonalizacaoPet.id_pet == pet.id_pet, PersonalizacaoPet.id_perso == p.id_perso).first()

            if p.tipo_perso not in dict_personalizacoes:
                dict_personalizacoes[p.tipo_perso] = []
            dict_personalizacoes[p.tipo_perso].append({
                "id_perso": p.id_perso,
                "nome_perso": p.nome_perso,
                "url": p.url_img,
                "tipo": p.tipo_perso,
                "valor": p.preco,
            })
            if not personalizacao_pet:
                dict_personalizacoes[p.tipo_perso][-1]["liberado"] = False    
            else:
                dict_personalizacoes[p.tipo_perso][-1]["liberado"] = True

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
