# Imports
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import hashlib
import jwt
from datetime import datetime
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Usuario, Crianca, Token

# Router
router = APIRouter(
    prefix="/login",
    tags=["Login"],
    responses={404: {"description": "Not found"}},
)

# Função para criptografar a senha
def criptografar_senha(senha):
    # Codifica a senha em bytes
    senha_bytes = senha.encode('utf-8')
    # Criando o objeto hash
    sha256 = hashlib.sha256()
    # Atualizando o objeto hash com a senha em bytes
    sha256.update(senha_bytes)
    # Gerando o hash da senha
    senha_hash = sha256.hexdigest()
    return senha_hash

def verificar_senha(senha, senha_hash):
    # Criptografando a senha em bytes
    senha_digitada = criptografar_senha(senha)
    # Verificando se a senha está correta
    if senha_digitada == senha_hash:
        return True
    return False

def geraTokenA(nome_user, email, tipo_user, cpf):
    payload = {
        "nome_user": nome_user,
        "email": email,
        "tipo_user": tipo_user,
        "cpf": cpf
    }
    encoded_jwt = jwt.encode(payload, "FeedIt2024Maua", algorithm="HS256")
    return encoded_jwt

def geraTokenB(nome_crianca, senha):
    payload = {
        "nome_crianca": nome_crianca,
        "senha": senha
    }
    encoded_jwt = jwt.encode(payload, "FeedIt2024Maua", algorithm="HS256")
    return encoded_jwt

# Rota para realizar o login
@router.post("/")
async def login(request: Request):
    session = Conexao().session
    try:
        data = await request.json()
        # Verificando se os campos estão preenchidos
        if (not data['email'] or not data['nome']) and not data['senha']:
            return JSONResponse(content={"message": "Obrigatório preencher todos os campos!"}, status_code=400)
        # Verificando se o nome está vazio
        if data['nome'] == "":
            # Buscando o usuário no banco
            usuario = session.query(Usuario).filter(Usuario.email == data["email"]).first()
            # Verificando se o usuário existe
            if not usuario:
                return JSONResponse(content={"message": "Usuário não encontrado!"}, status_code=404)
            # Verificando se a senha está correta
            if not verificar_senha(data['senha'], usuario.senha):
                return JSONResponse(content={"message": "Senha incorreta!"}, status_code=401)
            token = geraTokenA(usuario.nome_user, usuario.email, usuario.tipo_user, usuario.cpf)
            select_token = session.query(Token).filter(Token.id_user == usuario.id_user).first()
            if select_token:
                session.delete(select_token)
                session.commit()
            insert_token = Token(id_user=usuario.id_user, token=token, created_at=datetime.now())
            session.add(insert_token)
            session.commit()
            # Retornando a mensagem de sucesso
            return JSONResponse(content={"message": "Login realizado com sucesso!",
                                         "token": token,
                                         "tipo": f"{usuario.tipo_user}",
                                         "id_usuario": f"{usuario.id_user}"}, 
                                         status_code=200)
        # Verificando se o email está vazio
        if data['email'] == "":
            # Buscando a criança no banco
            crianca = session.query(Crianca).filter(Crianca.nome_crianca == data["nome"]).first()
            if not crianca:
                return JSONResponse(content={"message": "Criança não encontrada!"}, status_code=404)
            # Verificando se a senha está correta
            if not verificar_senha(data['senha'], crianca.senha):
                return JSONResponse(content={"message": "Senha incorreta!"}, status_code=401)
            token = geraTokenB(crianca.nome_crianca, crianca.senha)
            select_token = session.query(Token).filter(Token.id_crianca == crianca.id_crianca).first()
            if select_token:
                session.delete(select_token)
                session.commit()
            insert_token = Token(id_crianca=crianca.id_crianca, token=token, created_at=datetime.now())
            session.add(insert_token)
            session.commit()
            # Retornando a mensagem de sucesso
            return JSONResponse(content={"message": "Login realizado com sucesso!",
                                         "token": token,
                                         "tipo": "C",
                                         "id_crianca": f"{crianca.id_crianca}"}, status_code=200)
    # Tratamento de exceção
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao realizar o login!", "error": str(e)})
    # Fechando a sessão
    finally:
        session.close()
