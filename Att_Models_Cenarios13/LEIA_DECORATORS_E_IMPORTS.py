"""
COLA RÁPIDA — leia antes de fazer a atividade dos cenários
(comentários no estilo da profe, igual aos arquivos da Aula 11)

=== IMPORT COM PONTO (from .) ===
Dentro da pasta models/:
    from . import db           → pega db do __init__.py DO MESMO APARTAMENTO
    from .base import X        → pega do arquivo base.py ao lado

No controller (fora de models/):
    from models import Cliente → SEM ponto, olha de fora pro pacote models/

=== @classmethod ===
    @classmethod
    def listar(cls):
        return cls.query.all()

Chama: Filme.listar()   ← fala com a CLASSE inteira
cls = a própria classe (Filme, Cliente, etc.)

=== @property ===
    @property
    def total(self):
        return self.quantidade * self.preco

Usa: produto.total   ← SEM parênteses, parece campo mas calcula na hora

=== @route (decorator Flask) ===
    @cinema_bp.route("/")
    def index():
        ...

O @ cola a URL no navegador nesta função. É decorator também!

=== BLUEPRINT ===
    cinema_bp = Blueprint("cinema", __name__, url_prefix="/cinema")

Blueprint = pacote de rotas com apelido. Organiza o projeto:
  - app.py só REGISTRA: app.register_blueprint(cinema_bp)
  - cinema_controller.py tem as rotas de cinema
  - url_for('cinema.index') → apelido do Blueprint + nome da função

Analogia: o Flask é o prédio; cada Blueprint é um andar (clientes, pedidos, cinema).

=== self vs cls ===
    self  → este objeto aqui (um registro específico)
    cls   → o molde / a classe inteira
"""
