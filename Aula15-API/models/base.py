# Superclasse abstrata (Aula 11): campos comuns a todos os Models.
# __abstract__ = True → NÃO cria tabela própria; só herança.

from datetime import datetime

from . import db


class ModeloBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,  # atualiza sozinho em cada alteração
        nullable=False,
    )
