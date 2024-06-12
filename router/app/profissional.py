from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os

from sqlalchemy import func
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Usuario, UsuarioCrianca, Crianca, PetGrupoAlimento, GrupoAlimentos, Pet
# Router
router = APIRouter(
    prefix = "/profissional",
    tags = ["Profissional"],
    responses={404: {"description": "Not found"}},
)

# QuickSort
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivo = arr[len(arr) // 2]
    esq = [x for x in arr if x[1] > pivo[1] or (x[1] == pivo[1] and x[0] < pivo[0])]
    meio = [x for x in arr if x == pivo]
    dir = [x for x in arr if x[1] < pivo[1] or (x[1] == pivo[1] and x[0] > pivo[0])]
    return quicksort(esq) + meio + quicksort(dir)
# ------------------------------

@router.get("/{id_profissional}/pacientes")
async def listar_pacientes(id_profissional: int):
    session = Conexao().session
    try:
        select = session.query(Usuario).filter(Usuario.id_user == id_profissional).first()
        if not select:
            raise HTTPException(status_code=404, detail="Profissional não encontrado")
        select_pacientes = session.query(UsuarioCrianca).filter(UsuarioCrianca.id_user == id_profissional, UsuarioCrianca.relacao == 'P').all()
        pacientes = []
        for paciente in select_pacientes:
            select_crianca = session.query(Crianca).filter(Crianca.id_crianca == paciente.id_crianca).first()
            select_responsavel = session.query(UsuarioCrianca).filter(UsuarioCrianca.id_crianca == paciente.id_crianca, UsuarioCrianca.relacao == 'F').first()
            select_nome_responsavel = session.query(Usuario).filter(Usuario.id_user == select_responsavel.id_user).first()
            pacientes.append({"id_crianca": select_crianca.id_crianca, "nome_crianca": select_crianca.nome_crianca, "nome_responsavel": select_nome_responsavel.nome_user})
        return JSONResponse(content={"message": "Pacientes listados com sucesso!", "pacientes": pacientes, "medico": select.nome_user})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao listar os pacientes!", "error": str(e)})
    finally:
        session.close()

@router.get("/paciente/{id_paciente}")
async def listar_paciente(id_paciente: int):
    session = Conexao().session
    try:
        result = (session.query(GrupoAlimentos.grupo, func.count(PetGrupoAlimento.id_grupo))
          .join(PetGrupoAlimento, GrupoAlimentos.id == PetGrupoAlimento.id_grupo)
          .join(Pet, Pet.id_pet == PetGrupoAlimento.id_pet)
          .filter(Pet.id_crianca == id_paciente)
          .group_by(GrupoAlimentos.grupo)
          .all())
        dict_alimentos = {}
        for grupo, count in result:
            dict_alimentos[grupo] = count

        alimentos_list = list(dict_alimentos.items())
        lista_organizada = quicksort(alimentos_list)
        dict_alimentos_organizado = {k: v for k, v in lista_organizada}
        
        return JSONResponse(content={"message": "Infos do paciente listadas com sucesso!", "alimentos": dict_alimentos_organizado})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao listar o paciente!", "error": str(e)})
    finally:
        session.close()

@router.post("/vincula")
async def vincular_paciente(request: Request):
    session = Conexao().session
    try:
        data = await request.json()
        insert = UsuarioCrianca(id_user=data['id_profissional'], id_crianca=data['id_crianca'], relacao='P')
        session.add(insert)
        session.commit()
        return JSONResponse(content={"message": "Paciente vinculado com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao vincular o paciente!", "error": str(e)})
    finally:
        session.close()
