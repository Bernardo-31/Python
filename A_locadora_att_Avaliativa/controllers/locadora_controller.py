from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for

# Import SEM ponto — controller fica fora de models/
from models import ClienteLocadora, Locacao, Veiculo

# Blueprint "locadora" — grupo de rotas; url_prefix faz tudo começar com /locadora/
locadora_bp = Blueprint("locadora", __name__, url_prefix="/locadora")


# @route = decorator: esta URL chama a função logo abaixo
@locadora_bp.route("/")
def index():
    locacoes = Locacao.listar_com_detalhes()
    return render_template("locadora/lista.html", locacoes=locacoes)


@locadora_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    clientes = ClienteLocadora.listar()
    veiculos = Veiculo.listar()

    if request.method == "POST":
        cliente_id = request.form.get("cliente_id", "").strip()
        veiculo_id = request.form.get("veiculo_id", "").strip()
        data_inicio = request.form.get("data_inicio", "").strip()
        data_fim = request.form.get("data_fim", "").strip()
        valor_total = request.form.get("valor_total", "").strip()

        if not cliente_id or not veiculo_id or not data_inicio or not data_fim or not valor_total:
            return render_template(
                "locadora/formulario.html",
                clientes=clientes,
                veiculos=veiculos,
                erro="Preencha todos os campos.",
            )

        data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
        data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
        valor_total = float(valor_total)

        Locacao.salvar(cliente_id, veiculo_id, data_inicio, data_fim, valor_total)
        return redirect(url_for("locadora.index"))

    return render_template(
        "locadora/formulario.html",
        clientes=clientes,
        veiculos=veiculos,
    )
