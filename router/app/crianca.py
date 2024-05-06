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
    prefix = "/crianca",
    tags = ["Crianca"],
    responses={404: {"description": "Not found"}},
)

@router.get("/listar_personalizacao")
async def listar_personalizacao():
    session = Conexao().session
    try:
        personalizacoes = session.query(Personalizacao).all()
        return personalizacoes
    finally:
        session.close()