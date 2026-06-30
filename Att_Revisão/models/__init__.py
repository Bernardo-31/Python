from flask_sqlalchemy import SQLAlchemy

# Instancia central do SQLAlchemy.
# Ela e importada pelos modelos e inicializada em app.py com db.init_app(app).
db = SQLAlchemy()

# Estes imports deixam as classes disponiveis com: from models import Jogador, db.
from .base import ModeloBase
from .jogador import Jogador
