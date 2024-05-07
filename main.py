# Imports
import os
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database.sqlalchemy import cria_tabelas
from database.conexao import Conexao

# Rotas
from router.app import cadastro
from router.app import crianca
from router.app import img_recog
from router.app import login
from router.app import profissional
from router.app import responsavel

# FastAPI
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
] 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include das rotas
app.include_router(cadastro.router)
app.include_router(crianca.router)
app.include_router(img_recog.router)
app.include_router(login.router)
app.include_router(profissional.router)
app.include_router(responsavel.router)

# Teste de conexão
@app.get("/")
async def root():
    try:
        # cria_tabelas()
        Conexao()
        return JSONResponse(content={"message": "Conexão com o banco de dados realizada com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao conectar com o banco de dados!", "error": str(e)})
    finally:
        Conexao().fecha_conexao()

# Inicialização
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)