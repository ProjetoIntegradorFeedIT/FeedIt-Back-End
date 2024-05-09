# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
from openai import OpenAI
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
        data = await request.json()

        client = OpenAI()

        response = client.chat.completions.create(
          model="gpt-4-turbo",
          messages=[
            {
              "role": "user",
              "content": [
                {"type": "text", 
                 "text": 
                 "Please provide an image of a food item. Upon analysis, the system will return a dictionary with the following structure: dict = {'food': '', 'group': ''} Where: 'food' receives the name of the food contained in the image. And 'group' receives the food group to which this item belongs, and can take one of the following values: Fruits, Vegetables and greens, Meat and eggs, Cereals, tubers, bread and roots, Legumes, Milk and dairy products, Sweets, Snacks, Fungus. If the image is not a food, 'Not a food' will be returned for both key values. I just want you to return me a dictionary already filled"},
                {
                  "type": "image_url",
                  "image_url": {
                    "url": data["imagem"],
                  },
                },
              ],
            }
          ],
          max_tokens=100,
        )

        # "```json\n{\n  \"food\": \"Grilled salmon\",\n  \"group\": \"Meat and eggs\"\n}\n```"
        # "```json\n{\n  \"food\": \"Feijoada\",\n  \"group\": \"Legumes\"\n}\n```"
        
        teste = response.choices[0]
        return teste
        return JSONResponse(content={"message": "Imagem verificada com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao verificar a imagem!", "error": str(e)})
    finally:
        session.close()