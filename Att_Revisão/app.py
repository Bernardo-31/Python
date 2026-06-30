import os

from flask import Flask

# RESUMO DO QUE FOI COMPLETADO PARA O PROJETO RODAR:
#
# Antes, o codigo ja tentava importar "controllers" e "models", mas esses
# pacotes ainda nao existiam de verdade na estrutura do projeto. Tambem havia
# arquivos soltos na raiz, templates fora da pasta esperada pelo Flask e alguns
# trechos incompletos nos models/controllers.
#
# O que foi ajustado:
# 1. Criei a pasta controllers/ e movi as rotas para blueprints.
# 2. Criei a pasta models/ e coloquei nela o db, ModeloBase e Jogador.
# 3. Criei views/templates/ para os arquivos HTML.
# 4. Criei views/static/css/ para o arquivo CSS.
# 5. Corrigi o model Jogador, que estava sem nome da tabela e sem colunas.
# 6. Corrigi ModeloBase, que estava com "__abstract__ =" incompleto.
# 7. Corrigi dashboard_controller.py, que usava dashboard_bp sem ter criado.
# 8. Registrei tambem jogador_bp no app, pois antes so o dashboard estava registrado.
# 9. Corrigi templates quebrados, como extends incompleto e loop sem endfor.

# Os blueprints ficam no pacote controllers para separar as rotas do arquivo principal.
from controllers import dashboard_bp, jogador_bp
from dados_jogadores import popular_dados
# O objeto db fica no pacote models para ser compartilhado por todos os modelos.
from models import db


def criar_app():
    # Cria a aplicacao Flask e informa onde estao os templates e arquivos estaticos.
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    # Monta o caminho absoluto do banco SQLite dentro da pasta do projeto.
    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "jogadores.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Liga o SQLAlchemy ao app Flask.
    db.init_app(app)

    # Registra as rotas separadas em controllers.
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(jogador_bp)

    # Abre o contexto do Flask para criar as tabelas e popular dados iniciais.
    with app.app_context():
        db.create_all()
        popular_dados()

    return app


# Instancia usada quando o Flask importa este arquivo.
app = criar_app()

if __name__ == "__main__":
    # Executa o servidor de desenvolvimento ao rodar: python app.py
    app.run(debug=True)
