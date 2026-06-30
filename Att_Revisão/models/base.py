from datetime import datetime

from . import db


class ModeloBase(db.Model):
    # Classe abstrata: o SQLAlchemy nao cria tabela para ela.
    # Ela serve apenas para reaproveitar campos comuns nos outros modelos.
    __abstract__ = True

    # Campos herdados por todas as tabelas que usarem ModeloBase.
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
