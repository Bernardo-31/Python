# Aula 15 — ponto de entrada da API REST.
# Atenção: neste projeto NÃO usamos render_template nem pastas views/.
# Toda resposta é JSON (jsonify). Teste no Postman, Insomnia ou curl.

import os

from flask import Flask, jsonify

from controllers import livros_api_bp
from models import Livro, db

# Dados só para a primeira execução (banco vazio).
DADOS_INICIAIS = [
    ("Dom Casmurro", "Machado de Assis", 1899),
    ("O Cortiço", "Aluísio Azevedo", 1890),
    ("1984", "George Orwell", 1949),
]

# Documentação mínima — a rota GET / devolve isso em JSON.
ENDPOINTS = [
    {"metodo": "GET", "rota": "/api/livros", "descricao": "Listar todos os livros"},
    {"metodo": "GET", "rota": "/api/livros/<id>", "descricao": "Detalhe de um livro"},
    {"metodo": "POST", "rota": "/api/livros", "descricao": "Criar livro (JSON no body)"},
    {"metodo": "PUT", "rota": "/api/livros/<id>", "descricao": "Atualizar livro"},
    {"metodo": "DELETE", "rota": "/api/livros/<id>", "descricao": "Excluir livro"},
]


def criar_app():
    # Sem template_folder / static_folder: não há HTML nesta aula.
    app = Flask(__name__)

    pasta = os.path.abspath(os.path.dirname(__file__))
    # SQLite local — arquivo biblioteca.db na pasta do projeto.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        pasta, "biblioteca.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "aula15-api-rest-dev"

    db.init_app(app)
    # Registra só o Blueprint da API (prefixo /api).
    app.register_blueprint(livros_api_bp)

    with app.app_context():
        db.create_all()
        # Seed: se a tabela estiver vazia, grava os 3 livros iniciais.
        if Livro.query.count() == 0:
            for titulo, autor, ano in DADOS_INICIAIS:
                db.session.add(Livro(titulo=titulo, autor=autor, ano=ano))
            db.session.commit()

    @app.route("/")
    def index():
        # Também é JSON — não é uma "home" HTML, só um guia dos endpoints.
        return jsonify(
            {
                "aula": "15 — API REST (somente JSON)",
                "mensagem": "Use Postman, Insomnia ou curl. Não há páginas HTML neste projeto.",
                "endpoints": ENDPOINTS,
            }
        )

    return app


app = criar_app()

if __name__ == "__main__":
    # debug=True recarrega o servidor ao salvar o código (só para estudo).
    app.run(debug=True)
