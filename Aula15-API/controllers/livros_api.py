# Controller da API REST — aqui NÃO existe render_template.
# Cada rota busca no Model e devolve JSON com jsonify().
# Cliente típico: Postman, app mobile, outro backend — não o navegador com Jinja.

from flask import Blueprint, jsonify, request

from models import Livro, db

# url_prefix="/api" → todas as rotas abaixo começam com /api
# Ex.: /livros vira GET /api/livros
livros_api_bp = Blueprint("livros_api", __name__, url_prefix="/api")


@livros_api_bp.route("/livros", methods=["GET"])
def listar():
    # GET = ler/listar. Mesma consulta do Model; saída é lista de dicts em JSON.
    # Nas aulas de site seria: return render_template("lista.html", ...)
    # Aqui: jsonify([...])
    return jsonify([livro.para_dict() for livro in Livro.listar()])


@livros_api_bp.route("/livros/<int:livro_id>", methods=["GET"])
def detalhe(livro_id):
    # GET /api/livros/5 → um recurso específico.
    livro = db.session.get(Livro, livro_id)

    if not livro:
        # Na API não há página "404 HTML". Mandamos JSON + status 404.
        return jsonify({"erro": "Livro não encontrado"}), 404

    return jsonify(livro.para_dict())


@livros_api_bp.route("/livros", methods=["POST"])
def criar():
    # POST = criar. O body vem em JSON, NÃO em formulário HTML (request.form).
    dados = request.get_json()

    if not dados:
        # 400 = o cliente enviou a requisição errada (faltou JSON).
        return jsonify(
            {"erro": "Envie JSON no body (Content-Type: application/json)"}
        ), 400

    try:
        # Model monta o objeto a partir do dict (campos: titulo, autor, ano).
        livro = Livro.a_partir_de_dict(dados)
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    if not livro.titulo or not livro.autor:
        return jsonify({"erro": "Título e autor não podem ser vazios"}), 400

    # Persistência igual às outras aulas: add + commit.
    db.session.add(livro)
    db.session.commit()

    # 201 Created = "criei um recurso novo" (convenção REST).
    return jsonify(livro.para_dict()), 201


@livros_api_bp.route("/livros/<int:livro_id>", methods=["PUT"])
def atualizar(livro_id):
    # PUT = atualizar. Atualiza só os campos que vierem no JSON.
    livro = db.session.get(Livro, livro_id)
    if not livro:
        return jsonify({"erro": "Livro não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Envie JSON no body"}), 400

    try:
        livro.atualizar_de_dict(dados)
    except (ValueError, TypeError):
        return jsonify({"erro": "Campo ano deve ser um número inteiro"}), 400

    db.session.commit()
    # 200 OK + objeto atualizado (sem redirect, sem flash message).
    return jsonify(livro.para_dict())


@livros_api_bp.route("/livros/<int:livro_id>", methods=["DELETE"])
def excluir(livro_id):
    # DELETE = remover.
    livro = db.session.get(Livro, livro_id)
    if not livro:
        return jsonify({"erro": "Livro não encontrado"}), 404

    db.session.delete(livro)
    db.session.commit()

    # 204 No Content = deu certo, mas a resposta NÃO tem corpo.
    return "", 204
