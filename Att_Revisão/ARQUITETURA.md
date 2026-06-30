# Arquitetura do projeto

Este projeto e uma aplicacao Flask simples para cadastrar, listar, editar e excluir jogadores da selecao.

A organizacao foi separada em camadas para ficar mais facil entender e alterar:

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
        +-- index.html
        +-- layout.html
        +-- jogadores/
            +-- formulario.html
            +-- lista.html
```

## O que estava incompleto antes

O projeto tinha a ideia de uma arquitetura separada, mas varias partes ainda nao estavam conectadas ou estavam incompletas. Por isso, mesmo parecendo que o app ja tinha models, controllers e views, o Flask nao conseguiria rodar corretamente.

Principais problemas encontrados:

- `app.py` importava `controllers` e `models`, mas as pastas `controllers/` e `models/` ainda nao existiam como pacotes organizados.
- Os arquivos `jogador_controller.py`, `dashboard_controller.py`, `jogador.py`, `base.py`, HTML e CSS estavam todos soltos na raiz.
- `dashboard_controller.py` usava `dashboard_bp`, mas esse blueprint nao tinha sido criado.
- `app.py` registrava o `dashboard_bp`, mas nao registrava o `jogador_bp`, entao as rotas de jogadores nao ficariam disponiveis.
- `base.py` tinha `__abstract__ =` incompleto, o que quebra a sintaxe e impede o Python de importar o arquivo.
- `jogador.py` tinha ` = "jogadores"` incompleto no lugar de `__tablename__ = "jogadores"`.
- `jogador.py` nao tinha as colunas do banco, como `nome`, `posicao`, `clube`, `cabeceio` e `forca`.
- `index.html` tinha `{% extends " %}`, ou seja, nao apontava para o template base.
- `lista.html` abria um loop `{% for j in jogadores %}`, mas nao fechava com `{% endfor %}`.
- O CSS estava na raiz, mas o `layout.html` procurava o arquivo em `static/css/estilo.css`.

## O que eu alterei antes do codigo conseguir rodar

### 1. Separei os controllers

Criei a pasta `controllers/`.

Dentro dela ficaram:

- `dashboard_controller.py`: cuida da rota inicial `/`;
- `jogador_controller.py`: cuida das rotas `/jogadores`, cadastro, edicao e exclusao;
- `__init__.py`: junta os blueprints para o `app.py` importar com facilidade.

Antes, os controllers estavam soltos na raiz e nao formavam um pacote Python.

### 2. Corrigi o dashboard_controller.py

Antes ele tinha a rota:

```python
@dashboard_bp.route("/")
```

Mas `dashboard_bp` nao existia.

Agora ele cria o blueprint antes de usar:

```python
dashboard_bp = Blueprint("dashboard", __name__)
```

Sem isso, o Python daria erro porque tentaria usar uma variavel nao definida.

### 3. Separei os models

Criei a pasta `models/`.

Dentro dela ficaram:

- `__init__.py`: cria o `db = SQLAlchemy()`;
- `base.py`: cria a classe base com campos comuns;
- `jogador.py`: cria a tabela/model de jogadores.

Antes, o `app.py` fazia:

```python
from models import db
```

Mas nao existia um pacote `models` pronto para esse import funcionar corretamente.

### 4. Corrigi o ModeloBase

Antes estava incompleto:

```python
__abstract__ =
```

Corrigi para:

```python
__abstract__ = True
```

Isso diz ao SQLAlchemy que `ModeloBase` nao deve virar tabela. Ela so serve para passar campos comuns para outros models.

### 5. Corrigi o model Jogador

Antes o arquivo estava incompleto e faltava definir a tabela e as colunas.

Corrigi adicionando:

```python
__tablename__ = "jogadores"
```

E tambem as colunas:

```python
nome = db.Column(db.String(100), nullable=False)
posicao = db.Column(db.String(50), nullable=False)
clube = db.Column(db.String(100), nullable=False)
cabeceio = db.Column(db.Integer, nullable=False)
forca = db.Column(db.Integer, nullable=False)
```

Sem essas colunas, o formulario ate poderia enviar dados, mas o banco nao teria onde salvar `nome`, `clube`, `forca`, etc.

### 6. Registrei o blueprint de jogadores no app.py

Antes o app registrava so:

```python
app.register_blueprint(dashboard_bp)
```

Adicionei:

```python
app.register_blueprint(jogador_bp)
```

Sem isso, as rotas `/jogadores`, `/jogadores/cadastrar`, `/jogadores/editar/<id>` e `/jogadores/excluir/<id>` nao existiriam para o Flask.

### 7. Organizei os templates

Criei a pasta:

```text
views/templates/
```

E coloquei:

- `layout.html`;
- `index.html`;
- `jogadores/lista.html`;
- `jogadores/formulario.html`.

Isso combina com a configuracao do `app.py`:

```python
template_folder="views/templates"
```

### 8. Corrigi o index.html

Antes estava quebrado:

```jinja
{% extends " %}
```

Corrigi para:

```jinja
{% extends "layout.html" %}
```

Assim o `index.html` usa o layout base corretamente.

### 9. Corrigi a lista de jogadores

O template `lista.html` abria o loop:

```jinja
{% for j in jogadores %}
```

Mas faltava fechar:

```jinja
{% endfor %}
```

Sem isso, o Jinja daria erro ao renderizar a pagina.

### 10. Organizei o CSS

Criei a pasta:

```text
views/static/css/
```

E coloquei o CSS em:

```text
views/static/css/estilo.css
```

Isso combina com o `layout.html`:

```jinja
{{ url_for('static', filename='css/estilo.css') }}
```

E tambem com o `app.py`:

```python
static_folder="views/static"
```

### 11. Mantive os dados iniciais separados

O arquivo `dados_jogadores.py` continuou na raiz porque ele funciona como um script auxiliar do app.

Ele e chamado no `app.py` dentro do contexto da aplicacao:

```python
with app.app_context():
    db.create_all()
    popular_dados()
```

O `db.create_all()` cria as tabelas. Depois `popular_dados()` preenche jogadores iniciais somente se o banco estiver vazio.

## app.py

E o ponto de entrada da aplicacao.

Responsabilidades:

- cria o objeto Flask;
- configura onde ficam os templates e arquivos estaticos;
- configura o banco SQLite `jogadores.db`;
- inicializa o SQLAlchemy;
- registra as rotas vindas dos controllers;
- cria as tabelas no banco;
- chama `popular_dados()` para inserir jogadores iniciais se o banco estiver vazio;
- executa o servidor quando voce roda `python app.py`.

## controllers/

Controllers concentram as rotas da aplicacao. Eles recebem a requisicao do navegador, chamam os models quando precisam acessar dados e escolhem qual template sera exibido.

### controllers/__init__.py

Reune os blueprints para facilitar o import no `app.py`.

Assim o `app.py` consegue fazer:

```python
from controllers import dashboard_bp, jogador_bp
```

Depois, o `app.py` registra cada blueprint:

```python
app.register_blueprint(dashboard_bp)
app.register_blueprint(jogador_bp)
```

Esse jeito e simples para projetos pequenos, porque fica explicito quais blueprints estao sendo usados.

### controllers/dashboard_controller.py

Controla a pagina inicial `/`.

Ele consulta quantos jogadores existem:

```python
Jogador.query.count()
```

Depois envia esse total para o template `index.html`.

### controllers/jogador_controller.py

Controla as rotas de jogadores. Todas comecam com `/jogadores`.

Rotas principais:

- `/jogadores/`: lista todos os jogadores;
- `/jogadores/cadastrar`: mostra o formulario e salva novo jogador;
- `/jogadores/editar/<id>`: mostra o formulario preenchido e atualiza jogador;
- `/jogadores/excluir/<id>`: remove jogador.

O controller usa:

- `request.form` para ler dados enviados pelo formulario;
- `db.session.add()` para adicionar;
- `db.session.commit()` para salvar alteracoes;
- `db.session.delete()` para excluir;
- `redirect()` e `url_for()` para voltar para a listagem depois de salvar ou excluir.

## models/

Models representam as tabelas do banco e regras ligadas aos dados.

### models/__init__.py

Cria o objeto central do banco:

```python
db = SQLAlchemy()
```

Esse mesmo `db` e usado em todos os models e inicializado no `app.py`.

Tambem disponibiliza os models para imports mais simples:

```python
from models import Jogador, db
```

### models/base.py

Define `ModeloBase`, uma classe abstrata.

Ela nao cria uma tabela propria. Serve para reaproveitar campos comuns:

- `id`;
- `data_criacao`;
- `data_atualizacao`.

O `Jogador` herda esses campos automaticamente.

### models/jogador.py

Define o model `Jogador`, que representa a tabela `jogadores`.

Campos:

- `nome`;
- `posicao`;
- `clube`;
- `cabeceio`;
- `forca`.

Tambem possui:

- `media`: propriedade calculada com a media entre cabeceio e forca;
- `listar()`: metodo de classe que retorna jogadores ordenados por posicao e nome.

## views/

Contem a parte visual da aplicacao.

### views/templates/layout.html

Template base.

Ele contem a estrutura HTML comum das paginas:

- `html`;
- `head`;
- link para o CSS;
- menu de navegacao;
- bloco principal onde cada pagina coloca seu conteudo.

Os outros templates usam:

```jinja
{% extends "layout.html" %}
```

Isso evita repetir o mesmo HTML em todas as paginas.

### views/templates/index.html

Pagina inicial do sistema.

Mostra:

- titulo;
- quantidade total de jogadores;
- botao para acessar a listagem.

Recebe a variavel `total_jogadores` enviada pelo `dashboard_controller.py`.

### views/templates/jogadores/lista.html

Pagina de listagem.

Mostra uma tabela com todos os jogadores recebidos do controller.

Para cada jogador, exibe:

- nome;
- posicao;
- clube;
- cabeceio;
- forca;
- media;
- links para editar e excluir.

### views/templates/jogadores/formulario.html

Formulario usado para duas telas:

- cadastrar jogador;
- editar jogador.

Quando existe a variavel `jogador`, o formulario mostra os dados preenchidos para edicao.

Quando nao existe, ele aparece vazio para cadastro.

## views/static/css/estilo.css

Arquivo de estilos da aplicacao.

Controla:

- cores;
- menu;
- botoes;
- tabela;
- formulario;
- espacamentos.

Ele e carregado pelo `layout.html` com:

```jinja
{{ url_for('static', filename='css/estilo.css') }}
```

## dados_jogadores.py

Contem a funcao `popular_dados()`.

Essa funcao verifica se ja existem jogadores no banco. Se existir pelo menos um, ela para e nao faz nada.

Se o banco estiver vazio, ela cria uma lista inicial de jogadores e salva tudo com:

```python
db.session.add_all(jogadores)
db.session.commit()
```

## requirements.txt

Lista as dependencias do projeto:

```text
flask
flask-sqlalchemy
```

Para instalar:

```powershell
pip install -r requirements.txt
```

## Fluxo da aplicacao

1. Voce executa `python app.py`.
2. O Flask cria a aplicacao.
3. O banco SQLite e configurado.
4. Os blueprints sao registrados.
5. As tabelas sao criadas.
6. Dados iniciais sao inseridos se o banco estiver vazio.
7. O navegador acessa uma rota.
8. O controller responde renderizando um template.
9. O template mostra os dados na tela.

## O que foi corrigido na reorganizacao

- Foram criadas pastas separadas para `controllers`, `models`, `templates` e `static`.
- Os arquivos soltos da raiz foram movidos para suas camadas corretas.
- O blueprint `dashboard_bp` foi criado corretamente.
- O blueprint `jogador_bp` passou a ser registrado no `app.py`.
- O model `ModeloBase` recebeu `__abstract__ = True`.
- O model `Jogador` recebeu `__tablename__` e suas colunas.
- O template `index.html` passou a herdar corretamente de `layout.html`.
- A listagem de jogadores passou a fechar o loop `{% endfor %}` corretamente.
- O CSS foi colocado em `views/static/css/estilo.css`.

## Como rodar

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Execute:

```powershell
python app.py
```

Depois acesse no navegador:

```text
http://127.0.0.1:5000
```
