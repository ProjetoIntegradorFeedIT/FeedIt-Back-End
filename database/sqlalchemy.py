from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, TIMESTAMP, Date
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

# Importando o dotenv para pegar a string de conexão
import os
from dotenv import load_dotenv
load_dotenv()
connect = os.getenv("CONNECT")

# Importando o caminho do certificado
caminho = os.path.abspath(os.path.join(os.getcwd(), './database/ca.pem'))

# Conexão
engine = create_engine(connect, echo=True, connect_args={'ssl': {'ca': caminho}})
# engine.execute(...)

# Sessão
Session = sessionmaker(bind=engine)
session = Session()

# Base
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String(14), nullable=False, unique=True)
    crm = Column(String(15))
    tipo_user = Column(String(1), nullable=False)
    nome_user = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    senha = Column(String(200), nullable=False)
    finalizou_crianca = Column(Integer, default=0)

class Crianca(Base):
    __tablename__ = 'criancas'
    id_crianca = Column(Integer, primary_key=True, autoincrement=True)
    nome_crianca = Column(String(50), nullable=False)
    senha = Column(String(200), nullable=False)
    nivel = Column(Integer, default=1)
    xp_atual = Column(Integer, default=0)
    xp_necessario = Column(Integer, default=100)
    dinheiro = Column(Integer, default=0)

class UsuarioCrianca(Base):
    __tablename__ = 'usuario_criancas'
    id_vinculacao = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('usuarios.id_user'))
    id_crianca = Column(Integer, ForeignKey('criancas.id_crianca'))
    user = relationship("Usuario", back_populates="criancas")
    crianca = relationship("Crianca", back_populates="usuarios")

Usuario.criancas = relationship("UsuarioCrianca", back_populates="user")
Crianca.usuarios = relationship("UsuarioCrianca", back_populates="crianca")

class Pet(Base):
    __tablename__ = 'pets'
    id_pet = Column(Integer, primary_key=True, autoincrement=True)
    id_crianca = Column(Integer, ForeignKey('criancas.id_crianca'))
    nome_pet = Column(String(100), nullable=False)
    tipo_pet = Column(String(10), nullable=False)
    alimentacao = Column(Float, default=0)
    energia = Column(Float, default=0)
    felicidade = Column(Float, default=0)
    forca = Column(Float, default=0)
    alteracao = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())
    chapeu = Column(Integer, default=1)
    roupa = Column(Integer, default=1)
    cor = Column(Integer, default=1)
    fundo = Column(Integer, default=1)

class Personalizacao(Base):
    __tablename__ = 'personalizacoes'
    id_perso = Column(Integer, primary_key=True, autoincrement=True)
    nome_perso = Column(String(50), nullable=False)
    url_img = Column(String(255), nullable=False, unique=True)
    tipo_perso = Column(String(6), nullable=False)
    preco = Column(Integer)
    tipo_pet = Column(String(10), nullable=False)

class PersonalizacaoPet(Base):
    __tablename__ = 'personalizacao_pets'
    id_habilitacao = Column(Integer, primary_key=True, autoincrement=True)
    id_pet = Column(Integer, ForeignKey('pets.id_pet'))
    id_perso = Column(Integer, ForeignKey('personalizacoes.id_perso'))
    liberado = Column(Integer, default=0)
    pet = relationship("Pet", back_populates="personalizacoes")
    personalizacao = relationship("Personalizacao", back_populates="pets")

Pet.personalizacoes = relationship("PersonalizacaoPet", back_populates="pet")
Personalizacao.pets = relationship("PersonalizacaoPet", back_populates="personalizacao")

class Missao(Base):
    __tablename__ = 'missoes'
    id_missao = Column(Integer, primary_key=True, autoincrement=True)
    tipo_missao = Column(String(1), nullable=False)
    nome_missao = Column(String(50), nullable=False)
    valor = Column(Integer, nullable=False)
    tamanho = Column(Integer, nullable=False)

class CriancaMissao(Base):
    __tablename__ = 'crianca_missoes'
    id_tarefa = Column(Integer, primary_key=True, autoincrement=True)
    id_crianca = Column(Integer, ForeignKey('criancas.id_crianca'))
    id_missao = Column(Integer, ForeignKey('missoes.id_missao'))
    progresso_tarefa = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    prazo = Column(TIMESTAMP)
    crianca = relationship("Crianca", back_populates="tarefas")
    missao = relationship("Missao", back_populates="criancas")


Crianca.tarefas = relationship("CriancaMissao", back_populates="crianca")
Missao.criancas = relationship("CriancaMissao", back_populates="missao")

class Token(Base):
    __tablename__ = 'tokens'
    id_token = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('usuarios.id_user'))
    id_crianca = Column(Integer, ForeignKey('criancas.id_crianca'))
    token = Column(String(255), nullable=True)
    cod = Column(String(5), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    deleted_at = Column(TIMESTAMP)

class GrupoComidas(Base):
    __tablename__ = 'grupo_comidas'
    id_comida = Column(Integer, primary_key=True)
    grupo = Column(String(50))
    pnt_forca = Column(Float)
    pnt_alimentacao = Column(Float)
    pnt_felicidade = Column(Float)
    pnt_energia = Column(Float)

class Status(Base):
    __tablename__ = 'status'
    id_alter = Column(Integer, primary_key=True, autoincrement=True)
    atribuicao = Column(Date)
    pnt_forca = Column(Float)
    pnt_alimentacao = Column(Float)
    pnt_felicidade = Column(Float)
    pnt_energia = Column(Float)

def cria_tabelas():
    Base.metadata.create_all(engine)