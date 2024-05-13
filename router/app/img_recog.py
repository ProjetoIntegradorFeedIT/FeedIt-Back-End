# Imports
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
from openai import OpenAI
import base64

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

        # Decode the base64 image data
        image_data = base64.b64decode(data["imagem"])

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please provide an image of a food item. Upon analysis, the system will return a dictionary with the following structure: dict = {'food': '', 'group': ''} Where: 'food' receives the name of the food contained in the image. And 'group' receives the food group to which this item belongs, and can take one of the following values: Fruits, Vegetables and greens, Meat and eggs, Cereals, tubers, bread and roots, Legumes, Milk and dairy products, Sweets, Snacks, Fungus. If the image is not a food, 'Not a food' will be returned for both key values. I just want you to return me a dictionary already filled",
                        },
                        {
                            "type": "image",
                            "image": {
                                "data": image_data,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        string = response.choices[0].message.content
        formata = eval(string.replace('```json\n', '').replace('\n```', ''))

        if formata["food"] == "Not a food":
            return JSONResponse(content={"message": "Imagem não é um alimento!"})

        return formata
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao verificar a imagem!", "error": str(e)})
    finally:
        session.close()
