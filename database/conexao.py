from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importando o dotenv para pegar a string de conexão
import os
from dotenv import load_dotenv
load_dotenv()
connect = os.getenv("CONNECT")

# Importando o caminho do certificado
caminho = './database/ca.pem'
caminho_completo = os.path.abspath(os.path.join(os.getcwd(), caminho))

class Conexao:
    def __init__(self):
        self.engine = create_engine(connect, echo=True, connect_args={'ssl': {'ca': caminho_completo}})
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def fecha_conexao(self):
        self.session.close()
        self.engine.dispose()

    def get_conexao(self):
        return self.sessionq