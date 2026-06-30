# Passo a passo explicado para montar este projeto Flask

Este arquivo mostra como construir o projeto do zero e explica por que cada parte existe.

A ideia do sistema e simples: cadastrar, listar, editar e excluir jogadores. Para isso usamos:

- Flask: cria o site e as rotas;
- Flask-SQLAlchemy: faz a ligacao com o banco;
- SQLite: banco de dados local em um arquivo;
- Jinja: permite usar comandos dentro do HTML;
- CSS: deixa as telas com estilo.

## 1. Entenda a divisao do projeto

Antes de criar arquivos, entenda o papel de cada pasta:

```text
app.py
Arquivo principal. Liga Flask, banco, controllers, templates e dados iniciais.

controllers/
Guarda as rotas. Uma rota e um caminho do navegador, como /jogadores/.

models/
Guarda as classes que representam tabelas do banco.

views/templates/
Guarda os HTML renderizados pelo Flask.

views/static/
Guarda CSS, imagens e arquivos estaticos.

dados_jogadores.py
Insere dados iniciais no banco quando ele ainda esta vazio.
```

Essa separacao evita deixar tudo misturado em um arquivo so. Quando voce quiser mexer em tela, procura em `views`. Quando quiser mexer no banco, procura em `models`. Quando quiser mexer em URL, procura em `controllers`.

## 2. Estrutura final de pastas

A estrutura final fica assim:

```text
AtividadeRevisaoCopa/
+-- app.py
+-- dados_jogadores.py
+-- requirements.txt
+-- controllers/
|   +-- __init__.py
|   +-- dashboard_controller.py
|   +-- jogador_controller.py
+-- models/
|   +-- __init__.py
|   +-- base.py
|   +-- jogador.py
+-- views/
    +-- static/
    |   +-- css/
    |       +-- estilo.css
    +-- templates/
        +-- layout.html
        +-- index.html
        +-- jogadores/
            +-- lista.html
            +-- formulario.html
```

## 3. Criar o requirements.txt

O `requirements.txt` lista as bibliotecas que o projeto precisa.

```text
flask>=3.0
flask-sqlalchemy>=3.1
```

Para instalar:

```powershell
pip install -r requirements.txt
```

Se aparecer erro dizendo que `flask` nao existe, quase sempre e porque esse comando ainda nao foi executado no Python correto.

## 4. Criar os models

Models representam o banco de dados. Neste projeto, a tabela principal e `jogadores`, entao teremos uma classe chamada `Jogador`.

### 4.1. models/__init__.py

Esse arquivo cria o objeto central do banco:

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .base import ModeloBase
from .jogador import Jogador
```

O `db` fica aqui porque todos os models devem usar a mesma instancia do SQLAlchemy.

Importante: `db = SQLAlchemy()` ainda nao liga o banco ao Flask. Isso so acontece depois, no `app.py`, com:

```python
db.init_app(app)
```

Os imports finais permitem usar:

```python
from models import Jogador, db
```

em vez de importar cada arquivo separadamente.

### 4.2. models/base.py

Esse arquivo cria uma classe base com campos comuns:

```python
from datetime import datetime

from . import db


class ModeloBase(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now, nullable=False)
    data_atualizacao = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
    )
```

O mais importante:

```python
__abstract__ = True
```

Isso diz ao SQLAlchemy: "nao crie uma tabela para `ModeloBase`". Ela existe apenas para outras classes herdarem os campos `id`, `data_criacao` e `data_atualizacao`.

Se isso ficasse incompleto, como estava antes, o Python nem conseguiria importar o arquivo.

### 4.3. models/jogador.py

Esse arquivo cria a tabela de jogadores:

```python
from . import db
from .base import ModeloBase


class Jogador(ModeloBase):
    __tablename__ = "jogadores"

    nome = db.Column(db.String(100), nullable=False)
    posicao = db.Column(db.String(50), nullable=False)
    clube = db.Column(db.String(100), nullable=False)
    cabeceio = db.Column(db.Integer, nullable=False)
    forca = db.Column(db.Integer, nullable=False)

    @property
    def media(self):
        return (self.cabeceio + self.forca) / 2

    @classmethod
    def listar(cls):
        return cls.query.order_by(cls.posicao, cls.nome).all()
```

Explicando:

- `__tablename__ = "jogadores"` define o nome da tabela no banco;
- cada `db.Column(...)` define uma coluna;
- `nullable=False` significa campo obrigatorio;
- `media` nao e coluna, e uma propriedade calculada;
- `listar()` busca jogadores ordenados por posicao e nome.

Exemplo mental: quando voce faz isto:

```python
Jogador(nome="Neymar", posicao="Atacante", clube="Santos", cabeceio=7, forca=9)
```

voce cria um objeto Python. Quando adiciona esse objeto na `db.session` e faz `commit()`, ele vira uma linha no banco.

## 5. Criar os controllers

Controllers guardam as rotas. Eles recebem pedidos do navegador, conversam com os models se precisarem de dados, e escolhem qual template mostrar.

### 5.1. controllers/dashboard_controller.py

Esse controller cuida da pagina inicial:

```python
from flask import Blueprint, render_template

from models import Jogador

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    return render_template(
        "index.html",
        total_jogadores=Jogador.query.count(),
    )
```

Explicando:

- `Blueprint("dashboard", __name__)` cria um grupo de rotas chamado `dashboard`;
- `@dashboard_bp.route("/")` diz que a funcao abaixo responde pela URL `/`;
- `Jogador.query.count()` conta os jogadores no banco;
- `render_template("index.html", ...)` abre o HTML e envia variaveis para ele.

No template, a rota pode ser chamada assim:

```jinja
{{ url_for('dashboard.index') }}
```

Isso significa: blueprint `dashboard`, funcao `index`.

### 5.2. controllers/jogador_controller.py

Esse controller cuida de listar, cadastrar, editar e excluir:

```python
from flask import Blueprint, redirect, render_template, request, url_for

from models import Jogador, db

jogador_bp = Blueprint("jogador", __name__, url_prefix="/jogadores")
```

O `url_prefix="/jogadores"` significa que todas as rotas desse arquivo comecam com `/jogadores`.

Por exemplo:

```python
@jogador_bp.route("/cadastrar")
```

vira:

```text
/jogadores/cadastrar
```

#### Listar jogadores

```python
@jogador_bp.route("/")
def index():
    jogadores = Jogador.listar()
    return render_template("jogadores/lista.html", jogadores=jogadores)
```

Fluxo:

1. Usuario acessa `/jogadores/`.
2. Flask executa `index()`.
3. `Jogador.listar()` busca os dados.
4. O controller envia `jogadores` para o template.
5. `lista.html` monta a tabela.

#### Cadastrar jogador

```python
@jogador_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        jogador = Jogador(
            nome=request.form["nome"],
            posicao=request.form["posicao"],
            clube=request.form["clube"],
            cabeceio=int(request.form["cabeceio"]),
            forca=int(request.form["forca"]),
        )
        db.session.add(jogador)
        db.session.commit()
        return redirect(url_for("jogador.index"))

    return render_template("jogadores/formulario.html")
```

Essa rota faz duas coisas:

- com `GET`, mostra o formulario vazio;
- com `POST`, recebe os dados e salva.

`request.form["nome"]` pega o valor de um campo HTML assim:

```html
<input name="nome">
```

O nome do `input` precisa bater com o nome lido no controller.

Depois:

- `db.session.add(jogador)` prepara para salvar;
- `db.session.commit()` grava de verdade;
- `redirect(url_for("jogador.index"))` volta para a lista.

#### Editar jogador

```python
@jogador_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    jogador = db.session.get(Jogador, id)

    if request.method == "POST":
        jogador.nome = request.form["nome"]
        jogador.posicao = request.form["posicao"]
        jogador.clube = request.form["clube"]
        jogador.cabeceio = int(request.form["cabeceio"])
        jogador.forca = int(request.form["forca"])
        db.session.commit()
        return redirect(url_for("jogador.index"))

    return render_template("jogadores/formulario.html", jogador=jogador)
```

O `<int:id>` pega um numero da URL.

Exemplo:

```text
/jogadores/editar/5
```

Nesse caso, `id` vale `5`.

No `GET`, o formulario aparece preenchido. No `POST`, o jogador e atualizado.

#### Excluir jogador

```python
@jogador_bp.route("/excluir/<int:id>")
def excluir(id):
    jogador = db.session.get(Jogador, id)
    db.session.delete(jogador)
    db.session.commit()
    return redirect(url_for("jogador.index"))
```

Fluxo:

1. Pega o `id` pela URL.
2. Busca o jogador.
3. Remove com `delete`.
4. Confirma com `commit`.
5. Volta para a lista.

### 5.3. controllers/__init__.py

Esse arquivo reexporta os blueprints:

```python
from .dashboard_controller import dashboard_bp
from .jogador_controller import jogador_bp
```

Assim o `app.py` consegue fazer:

```python
from controllers import dashboard_bp, jogador_bp
```

Sem isso, voce teria que importar diretamente de cada arquivo de controller.

## 6. Criar o app.py

O `app.py` e o arquivo que monta a aplicacao:

```python
import os

from flask import Flask

from controllers import dashboard_bp, jogador_bp
from dados_jogadores import popular_dados
from models import db


def criar_app():
    app = Flask(
        __name__,
        template_folder="views/templates",
        static_folder="views/static",
    )

    pasta = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(pasta, "jogadores.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(jogador_bp)

    with app.app_context():
        db.create_all()
        popular_dados()

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
```

Explicando os pontos principais:

```python
template_folder="views/templates"
```

Diz onde ficam os HTML.

```python
static_folder="views/static"
```

Diz onde ficam CSS, imagens e outros arquivos estaticos.

```python
app.config["SQLALCHEMY_DATABASE_URI"] = ...
```

Configura o arquivo SQLite `jogadores.db`.

```python
db.init_app(app)
```

Liga o SQLAlchemy ao Flask.

```python
app.register_blueprint(dashboard_bp)
app.register_blueprint(jogador_bp)
```

Registra as rotas. Se esquecer uma dessas linhas, as rotas daquele controller nao funcionam.

```python
with app.app_context():
```

Abre o contexto da aplicacao. Isso e necessario para criar tabelas e usar o banco nesse momento.

```python
db.create_all()
```

Cria as tabelas que ainda nao existem.

```python
popular_dados()
```

Coloca dados iniciais se o banco estiver vazio.

## 7. Criar dados_jogadores.py

Esse arquivo serve para o sistema ja abrir com alguns jogadores cadastrados.

Estrutura:

```python
from models import Jogador, db


def popular_dados():
    if Jogador.query.count() > 0:
        return

    jogadores = [
        Jogador(nome="Alisson", posicao="Goleiro", clube="Liverpool", cabeceio=5, forca=7),
        Jogador(nome="Neymar", posicao="Atacante", clube="Santos", cabeceio=7, forca=9),
    ]

    db.session.add_all(jogadores)
    db.session.commit()
```

O trecho:

```python
if Jogador.query.count() > 0:
    return
```

evita duplicar jogadores toda vez que o app iniciar.

Sem isso, cada `python app.py` criaria os mesmos jogadores de novo.

## 8. Criar os templates

Templates sao HTML com Jinja.

Regras importantes:

- `{% ... %}` executa comandos, como `if`, `for`, `extends` e `block`;
- `{{ ... }}` mostra valores na tela.

### 8.1. layout.html

O `layout.html` e a base das telas.

Ele tem:

- estrutura HTML principal;
- link do CSS;
- menu;
- espaco para conteudo.

O link do CSS:

```jinja
<link rel="stylesheet" href="{{ url_for('static', filename='css/estilo.css') }}">
```

O bloco onde as paginas filhas entram:

```jinja
{% block content %}{% endblock %}
```

### 8.2. index.html

O `index.html` usa o layout:

```jinja
{% extends "layout.html" %}
```

E mostra o total de jogadores:

```jinja
{{ total_jogadores }}
```

Esse valor vem do `dashboard_controller.py`.

### 8.3. jogadores/lista.html

Esse template recebe uma lista chamada `jogadores`.

Ele percorre essa lista:

```jinja
{% for j in jogadores %}
    {{ j.nome }}
{% endfor %}
```

Cada `j` e um objeto `Jogador`.

Por isso podemos usar:

```jinja
{{ j.nome }}
{{ j.posicao }}
{{ j.media }}
```

Se esquecer o `{% endfor %}`, o Jinja da erro porque o loop ficou aberto.

### 8.4. jogadores/formulario.html

Esse mesmo formulario serve para cadastrar e editar.

No cadastro, o controller nao envia `jogador`, entao os campos ficam vazios.

Na edicao, o controller envia `jogador`, entao os campos ficam preenchidos.

Exemplo:

```jinja
value="{{ jogador.nome if jogador else '' }}"
```

Significa:

- se existe `jogador`, coloca o nome dele;
- se nao existe, coloca texto vazio.

Os campos do formulario precisam ter `name` igual ao que o controller le:

```html
<input type="text" name="nome">
```

combina com:

```python
request.form["nome"]
```

Se escrever `name="nome_jogador"` no HTML e `request.form["nome"]` no Python, vai dar erro.

## 9. Criar o CSS

O CSS fica em:

```text
views/static/css/estilo.css
```

Ele nao muda a logica do sistema, mas controla a aparencia:

- cores;
- menu;
- botoes;
- tabela;
- formulario;
- espacamento.

O Flask encontra o CSS porque no `app.py` existe:

```python
static_folder="views/static"
```

E no `layout.html` existe:

```jinja
url_for('static', filename='css/estilo.css')
```

## 10. Fluxo completo do sistema

### Abrir a lista

1. Usuario acessa `/jogadores/`.
2. Flask encontra o blueprint `jogador`.
3. Executa `index()` em `jogador_controller.py`.
4. Chama `Jogador.listar()`.
5. Busca jogadores no banco.
6. Renderiza `jogadores/lista.html`.
7. O navegador mostra a tabela.

### Cadastrar

1. Usuario acessa `/jogadores/cadastrar`.
2. Como e `GET`, o formulario aparece vazio.
3. Usuario preenche e envia.
4. O navegador faz `POST`.
5. O controller le `request.form`.
6. Cria um `Jogador`.
7. Salva com `db.session.add()` e `db.session.commit()`.
8. Redireciona para a lista.

### Editar

1. Usuario clica em editar.
2. A URL fica parecida com `/jogadores/editar/3`.
3. O controller pega `id = 3`.
4. Busca o jogador no banco.
5. Mostra formulario preenchido.
6. No envio, atualiza os campos.
7. Faz `commit()`.
8. Volta para a lista.

### Excluir

1. Usuario clica em excluir.
2. A URL envia o `id`.
3. O controller busca o jogador.
4. Remove com `db.session.delete()`.
5. Salva com `commit()`.
6. Volta para a lista.

## 11. Como rodar

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Rode:

```powershell
python app.py
```

Acesse:

```text
http://127.0.0.1:5000
```

## 12. Erros comuns e como pensar neles

### Erro: rota nao existe

Confira se o blueprint foi registrado no `app.py`:

```python
app.register_blueprint(jogador_bp)
```

### Erro: template nao encontrado

Confira:

- se o arquivo esta em `views/templates`;
- se o nome usado no `render_template()` esta igual;
- se `template_folder="views/templates"` esta no `app.py`.

### Erro: CSS nao carrega

Confira:

- se o CSS esta em `views/static/css/estilo.css`;
- se `static_folder="views/static"` esta no `app.py`;
- se o `layout.html` usa `url_for('static', filename='css/estilo.css')`.

### Erro: campo do formulario nao encontrado

Confira se o `name` do input bate com o `request.form`.

HTML:

```html
<input name="forca">
```

Python:

```python
request.form["forca"]
```

### Erro: dados nao salvam

Confira se existe:

```python
db.session.commit()
```

Sem `commit()`, a alteracao nao e gravada no banco.

## 13. Ordem recomendada para estudar

Leia nesta ordem:

1. `app.py`
2. `controllers/__init__.py`
3. `controllers/dashboard_controller.py`
4. `controllers/jogador_controller.py`
5. `models/__init__.py`
6. `models/base.py`
7. `models/jogador.py`
8. `dados_jogadores.py`
9. `views/templates/layout.html`
10. `views/templates/index.html`
11. `views/templates/jogadores/lista.html`
12. `views/templates/jogadores/formulario.html`
13. `views/static/css/estilo.css`

## 14. Perguntas para nao se perder

Quando estiver confuso, responda:

1. Qual URL eu estou acessando?
2. Qual controller recebe essa URL?
3. Qual funcao esta sendo executada?
4. Essa funcao usa qual model?
5. Ela renderiza qual template?
6. O template recebe quais variaveis?
7. Se for formulario, quais campos ele envia?
8. O controller le esses campos com quais nomes?

Se voce conseguir responder isso, voce entende o fluxo principal do projeto.

## 15. Como adicionar uma nova tela depois

Exemplo: criar uma tela de times.

1. Criar `models/time.py`.
2. Criar `controllers/time_controller.py`.
3. Criar um blueprint chamado `time_bp`.
4. Importar `time_bp` em `controllers/__init__.py`.
5. Importar e registrar `time_bp` no `app.py`.
6. Criar templates em `views/templates/times/`.
7. Testar a rota no navegador.

Esse e o motivo de separar a arquitetura: o projeto cresce sem virar bagunca.
