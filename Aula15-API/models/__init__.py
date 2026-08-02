# Pacote models: um único objeto db compartilhado + export dos Models.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Imports depois de criar db (evita import circular com base.py / livro.py).
from .base import ModeloBase
from .livro import Livro

__all__ = ["db", "ModeloBase", "Livro"]
