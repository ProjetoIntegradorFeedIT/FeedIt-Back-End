# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime, timedelta
# Import db connection
from sqlalchemy import func
from database.conexao import Conexao
from database.sqlalchemy import Crianca, Missao, CriancaMissao

# Router
router = APIRouter(
    prefix="/missoes",
    tags=["Missoes"],
    responses={404: {"description": "Not found"}},
)

# Gerenciar missões
@router.post("/gerenciar")
async def gerenciar_missoes(request: Request):
    session = Conexao().session
    try:
        data = await request.json()
        missoes = session.query(CriancaMissao).filter(CriancaMissao.id_crianca == data['id_crianca']).all()
        if len(missoes) == 0:
            # Selecionar missões diarias
            missoesD = session.query(Missao).filter(Missao.tipo_missao == 'D')
            missoesD = missoesD.order_by(func.random()).limit(2).all()
            # Selecionar missões semanais
            missoesS = session.query(Missao).filter(Missao.tipo_missao == 'S')
            missoesS = missoesS.order_by(func.random()).limit(3).all()
            current_time = datetime.now()
            for missao in missoesD:
                prazo = current_time + timedelta(days=1)
                session.add(CriancaMissao(id_crianca=data['id_crianca'], id_missao=missao.id_missao, progresso_tarefa=0, created_at=datetime.now(), prazo=prazo))
                session.commit()
            for missao in missoesS:
                prazo = current_time + timedelta(days=7)
                session.add(CriancaMissao(id_crianca=data['id_crianca'], id_missao=missao.id_missao, progresso_tarefa=0, created_at=datetime.now(), prazo=prazo))
                session.commit()
        else:
            for missao in missoes:
                select_missao = session.query(Missao).filter(Missao.id_missao == missao.id_missao).first()
                if select_missao.tipo_missao == 'D':
                    if missao.prazo < datetime.now():
                        session.delete(missao)
                        session.commit()
                        missoesD = session.query(Missao).filter(Missao.tipo_missao == 'D')
                        missoesD = missoesD.order_by(func.random()).limit(1).all()
                        for missao in missoesD:
                            session.add(CriancaMissao(id_crianca=data['id_crianca'], id_missao=missao.id_missao, progresso_tarefa=0, created_at=datetime.now(), prazo=datetime.now() + timedelta(days=1)))
                            session.commit()
                if select_missao.tipo_missao == 'S':
                    if missao.prazo < datetime.now():
                        session.delete(missao)
                        session.commit()
                        missoesS = session.query(Missao).filter(Missao.tipo_missao == 'S')
                        missoesS = missoesS.order_by(func.random()).limit(1).all()
                        for missao in missoesS:
                            session.add(CriancaMissao(id_crianca=data['id_crianca'], id_missao=missao.id_missao, progresso_tarefa=0, created_at=datetime.now(), prazo=datetime.now() + timedelta(days=7)))
                            session.commit()
        return JSONResponse(content={"message": "Missões gerenciadas!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao gerenciar missões!", "error": str(e)})
    finally:
        session.close()
