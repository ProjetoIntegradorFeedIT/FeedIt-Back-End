# Imports
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import requests
import os
import re
from openai import OpenAI

# import db connection
from database.conexao import Conexao
from database.sqlalchemy import PetGrupoAlimento, Pet, GrupoAlimentos, Crianca, CriancaMissao, Missao

# Router
router = APIRouter(
    prefix="/img_recog",
    tags=["Imagem_Reconhecimento"],
    responses={404: {"description": "Not found"}},
)

def xp(id_crianca):
    session = Conexao().session
    try:
        selec_crianca = session.query(Crianca).filter(Crianca.id_crianca == id_crianca).first()
        if (selec_crianca.xp_atual + 100 > selec_crianca.xp_necessario):
            selec_crianca.xp_atual = 0
            selec_crianca.xp_necessario += 100
            selec_crianca.nivel += 1
            session.commit()
        else:
            selec_crianca.xp_atual += 100
            session.commit()
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao alterar o xp!", "error": str(e), "status_code": 500})
    finally:
        session.close()

def missoes(id_crianca, grupo):
    session = Conexao().session
    try:
        missoes = session.query(CriancaMissao).filter(CriancaMissao.id_crianca == id_crianca).all()
        for missao in missoes:
            select_missao = session.query(Missao).filter(Missao.id_missao == missao.id_missao).first()
            nome = select_missao.nome_missao.split(" ")
            for i in nome:
                if i.lower() == grupo.lower():
                    if missao.concluida == 0 and missao.progresso_tarefa + 1 >= select_missao.tamanho:
                        missao.concluida = 1
                        session.commit()
                        xp(id_crianca)
                        select_crianca = session.query(Crianca).filter(Crianca.id_crianca == id_crianca).first()
                        select_crianca.dinheiro += select_missao.valor
                        session.commit()
                    elif missao.concluida == 0 and missao.progresso_tarefa + 1 < select_missao.tamanho:
                        missao.progresso_tarefa += 1
                        session.commit()
                    else:
                        pass
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao gerenciar missões!", "error": str(e), "status_code": 500})
    finally:
        session.close()

@router.post("/verificar")
async def verificar_imagem(request: Request):
    session = Conexao().session
    try:
        data = await request.json()

        client = OpenAI()

        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"
        }

        payload = {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "Por favor, forneça uma imagem de um item alimentar. Após a análise, o sistema retornará um dicionário com a seguinte estrutura: dict = {'comida': '', 'grupo': ''}. Onde: 'comida' receberá o nome do alimento contido na imagem. E 'grupo' receberá o grupo alimentar ao qual esse item pertence, e pode assumir um dos seguintes valores: Frutas, Vegetais e folhas, Carne e ovos, Cereais, tubérculos, pão e raízes, Legumes, Leite e laticínios, Doces, Petiscos, Fungos. Se a imagem não for de um alimento, 'Não é um alimento' será retornado para ambos os valores-chave. Eu só quero que você me retorne um dicionário já preenchido.",
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": data["imagem"],
                  }
                }
              ]
            }
          ],
          "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response = response.json()

        # resposnta para dicionario
        resposta = response.get("choices")[0].get("message").get("content")
        match = re.search(r"'grupo': '([^']*)'", resposta)
        if match and match.group(1) != "Não é um alimento":
            valor_grupo = match.group(1)

            select_grupo = session.query(GrupoAlimentos).filter(GrupoAlimentos.grupo == valor_grupo).first()
            select_pet = session.query(Pet).filter(Pet.id_crianca == data["id_crianca"]).first()
            if (select_pet.alimentacao + select_grupo.alimentacao) > 100:
                select_pet.alimentacao = 100
                session.commit()
            elif (select_pet.alimentacao + select_grupo.alimentacao) < -100:
                select_pet.alimentacao = -100
                session.commit()
            else:
                select_pet.alimentacao += select_grupo.alimentacao
                session.commit()
            if (select_pet.forca + select_grupo.forca) > 100:
                select_pet.forca = 100
                session.commit()
            elif (select_pet.forca + select_grupo.forca) < -100:
                select_pet.forca = -100
                session.commit()
            else:  
                select_pet.forca += select_grupo.forca
                session.commit()
            if (select_pet.felicidade + select_grupo.felicidade) > 100:
                select_pet.felicidade = 100
                session.commit()
            elif (select_pet.felicidade + select_grupo.felicidade) < -100:
                select_pet.felicidade = -100
                session.commit()
            else:
                select_pet.felicidade += select_grupo.felicidade
                session.commit()
            if (select_pet.energia + select_grupo.energia) > 100:
                select_pet.energia = 100
                session.commit()
            elif (select_pet.energia + select_grupo.energia) < -100:
                select_pet.energia = -100
                session.commit()
            else:
                select_pet.energia += select_grupo.energia
                session.commit()
            insert = PetGrupoAlimento(id_pet=select_pet.id_pet, id_grupo=select_grupo.id)
            session.add(insert)
            session.commit()

            missoes(data["id_crianca"], valor_grupo)
            xp(data["id_crianca"])

            valor_alimento = re.search(r"'comida': '([^']*)'", resposta).group(1)

            return JSONResponse(content={"status_code": 200, "message": "Imagem verificada com sucesso!", "grupo": valor_grupo, "alimento": valor_alimento, "alimentacaoSaudavel": select_grupo.alimentacao, "forca": select_grupo.forca, "felicidade": select_grupo.felicidade, "energia": select_grupo.energia})
        else:
            return JSONResponse(content={"status_code": 304, "message": "Opa, parece que isso não é um alimento, se a gente se enganou conta ai pra gente o que que é isso!"})
        
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao verificar a imagem!", "error": str(e), "status_code": 500})
    finally:
        session.close()

@router.post("/forceInput")
async def force_input(request: Request):
    session = Conexao().session
    try:
        data = await request.json()

        select_grupo = session.query(GrupoAlimentos).filter(GrupoAlimentos.grupo == data["grupo"]).first()
        select_pet = session.query(Pet).filter(Pet.id_crianca == data["id_crianca"]).first()
        if (select_pet.alimentacao + select_grupo.alimentacao) > 100:
            select_pet.alimentacao = 100
            session.commit()
        elif (select_pet.alimentacao + select_grupo.alimentacao) < -100:
            select_pet.alimentacao = -100
            session.commit()
        else:
            select_pet.alimentacao += select_grupo.alimentacao
            session.commit()
        if (select_pet.forca + select_grupo.forca) > 100:
            select_pet.forca = 100
            session.commit()
        elif (select_pet.forca + select_grupo.forca) < -100:
            select_pet.forca = -100
            session.commit()
        else:
            select_pet.forca += select_grupo.forca
            session.commit()
        if (select_pet.felicidade + select_grupo.felicidade) > 100:
            select_pet.felicidade = 100
            session.commit()
        elif (select_pet.felicidade + select_grupo.felicidade) < -100:
            select_pet.felicidade = -100
            session.commit()
        else:
            select_pet.felicidade += select_grupo.felicidade
            session.commit()
        if (select_pet.energia + select_grupo.energia) > 100:
            select_pet.energia = 100
            session.commit()
        elif (select_pet.energia + select_grupo.energia) < -100:
            select_pet.energia = -100
            session.commit()
        else:
            select_pet.energia += select_grupo.energia
            session.commit()
        insert = PetGrupoAlimento(id_pet=select_pet.id_pet, id_grupo=select_grupo.id)
        session.add(insert)

        missoes(data["id_crianca"], data["grupo"])
        xp(data["id_crianca"])

        return JSONResponse(content={"status_code": 200, "message": "Forçando input de dados!", "alimentacaoSaudavel": select_grupo.alimentacao, "forca": select_grupo.forca, "felicidade": select_grupo.felicidade, "energia": select_grupo.energia})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao forçar input de dados!", "error": str(e), "status_code": 500})
    finally:
        session.close()
