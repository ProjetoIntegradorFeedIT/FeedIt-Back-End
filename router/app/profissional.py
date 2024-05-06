from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao

# Router
router = APIRouter(
    prefix = "/profissional",
    tags = ["Profissional"],
    responses={404: {"description": "Not found"}},
)

# Depois remove o comentário
# O que fazer: Criar uma rota para listar todos os pacientes de um profissional
# Como? - Criar um endpoint GET /profissional/{id}/pacientes que recebe o id do profissional
# - Retornar um JSON com todos os pacientes do profissional
@router.get("/{id_profissional}/pacientes")
async def listar_pacientes(id_profissional: int):
    session = Conexao().session
    try:
        # Aqui vem o seu código
        return JSONResponse(content={"message": "Pacientes listados com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao listar os pacientes!", "error": str(e)})
    finally:
        session.close()

# Depois remove o comentário
# O que fazer: Criar uma rota para trazer os dados de um paciente de um profissional
# Como? - Criar um endpoint GET /profissional/{id_profissional}/paciente/{id_paciente} que recebe o id do profissional e o id do paciente
# - Retornar um JSON com os dados do paciente
@router.get("/{id_profissional}/paciente/{id_paciente}")
async def listar_paciente(id_profissional: int, id_paciente: int):
    session = Conexao().session
    try:
        # Aqui vem o seu código
        return JSONResponse(content={"message": "Paciente listado com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao listar o paciente!", "error": str(e)})
    finally:
        session.close()

# Depois remove o comentário
# O que fazer: Criar uma rota para listar todos os responsáveis de um paciente
# Como? - Criar um endpoint GET /profissional/{id_profissional}/paciente/{id_paciente}/responsaveis que recebe o id do profissional e o id do paciente
# - Retornar um JSON com todos os responsáveis do paciente
@router.get("/{id_profissional}/paciente/{id_paciente}/responsaveis")
async def listar_responsaveis(id_profissional: int, id_paciente: int):
    session = Conexao().session
    try:
        # Aqui vem o seu código
        return JSONResponse(content={"message": "Responsáveis listados com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao listar os responsáveis!", "error": str(e)})
    finally:
        session.close()

# Depois remove o comentário
# O que fazer: Criar uma rota para trazer os dados para a montagem do gráfico de evolução de um paciente
# Como? - Criar um endpoint GET /profissional/{id_profissional}/paciente/{id_paciente}/evolucao que recebe o id do profissional e o id do paciente
# - Retornar um JSON com os dados para a montagem do gráfico
@router.get("/{id_profissional}/paciente/{id_paciente}/evolucao")
async def listar_evolucao(id_profissional: int, id_paciente: int):
    session = Conexao().session
    try:
        # Aqui vem o seu código
        return JSONResponse(content={"message": "Evolução listada com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao listar a evolução!", "error": str(e)})
    finally:
        session.close()