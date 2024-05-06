from pydantic import BaseModel

# Exemplo de modelo de dados
class NomeDoModelo(BaseModel):
    # Atributos: Tipo
    id_usuario: int
    id_estabelecimento: int
    comentario: str
    nota: int