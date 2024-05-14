# Imports
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import requests
import os
from openai import OpenAI

# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao

# Router
router = APIRouter(
    prefix="/img_recog",
    tags=["Imagem_Reconhecimento"],
    responses={404: {"description": "Not found"}},
)

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
        return response.get("choices")[0].get("message").get("content")
        
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao verificar a imagem!", "error": str(e)})
    finally:
        session.close()
