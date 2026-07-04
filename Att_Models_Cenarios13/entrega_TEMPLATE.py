"""
ATIVIDADE AULA 11 — Models por cenário (1,0 ponto)

Aluno: _______________________________
Cenário escolhido (A, B ou C): _________
  A = Locadora de veículos
  B = Cinema
  C = Troca de figurinhas Copa do Mundo

Renomeie este arquivo para: models_cenario_SEU_CENARIO.py
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ModeloBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(
        db.DateTime, default=datetime.now, nullable=False
    )
    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )


# =============================================================================
# TODO ALUNO: crie pelo menos 3 tabelas abaixo, todas herdando ModeloBase
# Use db.ForeignKey("nome_tabela.id") para ligar as tabelas
# Use db.relationship() para navegar entre elas
# =============================================================================


class Tabela1(ModeloBase):
    __tablename__ = "___________"
    # campos específicos do seu cenário
    pass


class Tabela2(ModeloBase):
    __tablename__ = "___________"
    # TODO: chave estrangeira para Tabela1
    # tabela1_id = db.Column(db.Integer, db.ForeignKey("..."), nullable=False)
    pass


class Tabela3(ModeloBase):
    __tablename__ = "___________"
    # TODO: chave estrangeira(s)
    pass


# Opcional: 4ª tabela para cenários B (Ingresso) ou C (ItemOferta)
