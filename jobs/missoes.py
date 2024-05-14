# Imports
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import json
import os
from datetime import datetime, timedelta
# Import db connection
from sqlalchemy import func
from database.conexao import Conexao
from database.sqlalchemy import Personalizacao, Crianca, Pet, Missao, CriancaMissao

def gerencia_missoes():
    session = Conexao().session
    try:
        # Verificar se a criança tem missões
        criancas = session.query(Crianca).all()
        for crianca in criancas:
            # Verificar se a criança tem missões
            missoes = session.query(CriancaMissao).filter(CriancaMissao.id_crianca == crianca.id_crianca).all()
            if len(missoes) == 0:
                # Selecionar missões diarias
                missoesD = session.query(Missao).filter(Missao.tipo_missao == 'D')
                missoesD = missoesD.order_by(func.random()).limit(3).all()
                # Selecionar missões semanais
                missoesS = session.query(Missao).filter(Missao.tipo_missao == 'S')
                missoesS = missoesS.order_by(func.random()).limit(3).all()
                insert_missoes = []
                for missao in missoesD:
                    insert_missoes.append(CriancaMissao(id_crianca=crianca.id_crianca, id_missao=missao.id_missao, prazo=datetime.now().strftime('%Y-%m-%d %H:%M:%S')+timedelta(days=1)))
                for missao in missoesS:
                    insert_missoes.append(CriancaMissao(id_crianca=crianca.id_crianca, id_missao=missao.id_missao, prazo=datetime.now().strftime('%Y-%m-%d %H:%M:%S')+timedelta(days=7)))
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
                                insert_missoes.append(CriancaMissao(id_crianca=crianca.id_crianca, id_missao=missao.id_missao, prazo=datetime.now().strftime('%Y-%m-%d %H:%M:%S')+timedelta(days=1)))
                    if select_missao.tipo_missao == 'S':
                        if missao.prazo < datetime.now():
                            session.delete(missao)
                            session.commit()
                            missoesS = session.query(Missao).filter(Missao.tipo_missao == 'S')
                            missoesS = missoesS.order_by(func.random()).limit(1).all()
                            for missao in missoesS:
                                insert_missoes.append(CriancaMissao(id_crianca=crianca.id_crianca, id_missao=missao.id_missao, prazo=datetime.now().strftime('%Y-%m-%d %H:%M:%S')+timedelta(days=7)))
        return JSONResponse(content={"message": "Missões gerenciadas!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao gerenciar missões!", "error": str(e)})
    finally:
        session.close()

if __name__ == '__main__':
    gerencia_missoes()