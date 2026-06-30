from . import db
from .base import ModeloBase


class Jogador(ModeloBase):
    # Nome da tabela criada no banco SQLite.
    __tablename__ = "jogadores"

    # Colunas especificas da tabela jogadores.
    nome = db.Column(db.String(100), nullable=False)
    posicao = db.Column(db.String(50), nullable=False)
    clube = db.Column(db.String(100), nullable=False)
    cabeceio = db.Column(db.Integer, nullable=False)
    forca = db.Column(db.Integer, nullable=False)

    @property
    def media(self):
        # Propriedade calculada: nao vira coluna no banco.
        return (self.cabeceio + self.forca) / 2

    @classmethod
    def listar(cls):
        # Consulta todos os jogadores ordenados por posicao e nome.
        return cls.query.order_by(cls.posicao, cls.nome).all()
