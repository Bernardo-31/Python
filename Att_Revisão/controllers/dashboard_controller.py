from flask import Blueprint, render_template

from models import Jogador

# Blueprint do painel inicial. Como nao tem url_prefix, responde na raiz "/".
dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    # Renderiza a pagina inicial enviando o total de jogadores para o template.
    return render_template(
        "index.html",
        total_jogadores=Jogador.query.count(),
    )
