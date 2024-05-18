from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import hashlib
import smtplib
import datetime
import random
import string
import email.message
# Import db connection
from database.conexao import Conexao
from database.sqlalchemy import Usuario, Crianca, UsuarioCrianca, Token

# Router
router = APIRouter(
    prefix = "/cadastro",
    tags = ["Cadastro"],
    responses={404: {"description": "Not found"}},
)

def criptografar_senha(senha):
    senha_bytes = senha.encode('utf-8')
    sha256 = hashlib.sha256()
    sha256.update(senha_bytes)
    senha_hash = sha256.hexdigest()
    return senha_hash

@router.post("/responsavel")
async def cadastrar_usuario_responsavel(request: Request):
    session = Conexao().session
    try:
        data = await request.json()
        responsavel = session.query(Usuario).filter(Usuario.email == data['email']).first()
        if responsavel:
            return JSONResponse(content={"message": "Usuário já cadastrado!"})
        senha = criptografar_senha(data['senha'])
        novo_responsavel = Usuario(nome_user=data['nome'], email=data['email'], senha=senha, cpf=data['cpf'], tipo_user='R')
        session.add(novo_responsavel)
        session.commit()
        return JSONResponse(content={"message": "Usuário cadastrado com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao cadastrar o usuário!", "error": str(e)})
    finally:
        session.close()
    
@router.post("/responsavel_email")
async def cadastrar_usuario_responsavel_email(request: Request):
    session = Conexao().session
    try:
        data = await request.json()

        responsavel = session.query(Usuario).filter(Usuario.email == data['email']).first()
        if responsavel:
            return JSONResponse(content={"message": "Usuário já cadastrado!"})

        caracteres = string.ascii_letters + string.digits
        codigo = ''.join(random.choice(caracteres) for _ in range(5))

        insert = Token(cod=codigo, created_at=datetime.now())
        session.add(insert)
        session.commit()
        
        corpo_email = f"""
        <p>Código: {codigo}</p>
        """

        msg = email.message.Message()
        msg['Subject'] = "Seu Código de Verificação"
        msg['From'] = 'feeditemail@gmail.com'
        msg['To'] = data['email']
        password = 'yaql bljy xjzx qndj' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')

        return JSONResponse(content={"message": "Te enviamos um email para verificação!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao cadastrar o usuário!", "error": str(e)})
    finally:
        session.close()

@router.post("/responsavel_codigo")
async def cadastrar_usuario_responsavel_codigo(request: Request):
    session = Conexao().session
    try:
        data = await request.json()
        token = session.query(Token).filter(Token.cod == data['codigo']).first()
        if not token:
            return JSONResponse(content={"message": "Código inválido!"})
        responsavel = session.query(Usuario).filter(Usuario.email == data['email']).first()
        if responsavel:
            return JSONResponse(content={"message": "Usuário já cadastrado!"})
        senha = criptografar_senha(data['senha'])
        novo_responsavel = Usuario(nome_user=data['nome'], email=data['email'], senha=senha, cpf=data['cpf'], tipo_user='R')
        session.add(novo_responsavel)
        session.commit()
        return JSONResponse(content={"message": "Usuário cadastrado com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao cadastrar o usuário!", "error": str(e)})
    finally:
        session.close()

# Cadastro de profissional
@router.post("/profissional")
async def cadastrar_usuario_profissional(request: Request):
    session = Conexao().session
    try:
        data = await request.json()
        profissional = session.query(Usuario).filter(Usuario.crm == data['crm']).first()
        if profissional:
            return JSONResponse(content={"message": "Usuário já cadastrado!"})

        senha = criptografar_senha(data['senha'])

        corpo_email = f"""
        <p>Nome: {data['nome']}</p>
        <p>Email: {data['email']}</p>
        <p>Senha: {senha}</p>
        <p>CRM: {data['crm']}</p>
        """

        msg = email.message.Message()
        msg['Subject'] = "Novo Usuário Profissional"
        msg['From'] = 'feeditemail@gmail.com'
        msg['To'] = 'feeditemail@gmail.com'
        password = 'yaql bljy xjzx qndj' 
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email )

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        print('Email enviado')

        return JSONResponse(content={"message": "Tudo certo! Após a verificação do CRM, o médico será cadastrado"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao cadastrar o usuário!", "error": str(e)})
    finally:
        session.close()

@router.post("/crianca")
async def cadastrar_usuario_crianca(request: Request):
    session = Conexao().session
    try:
        data = await request.json()
        nova_crianca = Crianca(nome_crianca=data['nome'], senha=criptografar_senha(data['senha']))
        session.add(nova_crianca)
        session.commit()
        nova_relacao = UsuarioCrianca(id_user=data['id_user'], id_crianca=nova_crianca.id_crianca)
        session.add(nova_relacao)
        session.commit()
        return JSONResponse(content={"message": "Usuário cadastrado com sucesso!"})
    except Exception as e:
        return JSONResponse(content={"message": "Erro ao cadastrar o usuário!", "error": str(e)})
    finally:
        session.close()