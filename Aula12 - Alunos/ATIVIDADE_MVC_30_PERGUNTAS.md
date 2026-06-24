# Atividade Aula 12 — Model, Controller e View (StreamFlix)

**Disciplina:** Python / Flask  
**Profª:** Janaína Duarte  
**Projeto:** `flask/Aula12/`  
**Objetivo:** Explorar o código, localizar arquivos e explicar o que cada camada faz.

---

## Como responder

1. Abra a pasta `flask/Aula12/` no editor ou GitHub.
2. Navegue pelas pastas `models/`, `controllers/` e `views/`.
3. Rode o site (`python app.py`) quando a pergunta pedir para testar no navegador.
4. Responda com **caminho do arquivo** + **explicação em suas palavras**.

**Identificação**

- Nome: _______________________________
- Turma: _______________________________

---

## Bloco A — Model (perguntas 1 a 10)

**1.** Em qual pasta ficam as classes que representam tabelas do banco SQLite? Cite o caminho.
As classes que representam tabelas do banco ficam na pasta: models/

**2.** Qual é o nome do arquivo de banco criado quando o app roda? Em qual arquivo Python essa configuração está?
O banco criado é: streamflix.db
A configuração está em: app.py

**3.** Quais classes Model existem no projeto (nome das classes)? Em quais arquivos `.py` cada uma está?
Classes: FilmeFavorito,  HistoricoBusca,  ModeloBase
Arquivos: models/filme_favorito.py,  models/historico_busca.py,   models/base.py

**4.** De qual superclasse `FilmeFavorito` e `HistoricoBusca` herdam? O que elas ganham automaticamente por herança (cite 3 campos)?
As duas classes herdam de: ModeloBase
Campos herdados automaticamente: id, data_criacao, data_atualizacao

**5.** Qual é o `__tablename__` da tabela de favoritos? Por que usamos `__tablename__` em vez de só o nome da classe?
__tablename__ = "filmes_favoritos"
Usamos __tablename__ para definir explicitamente o nome da tabela no banco, independentemente do nome da classe Python.

**6.** No model `FilmeFavorito`, qual coluna guarda o id do filme vindo da API TMDB? Ela tem alguma restrição especial (`unique`, `nullable`)?
A coluna que guarda o id da TMDB é: tmdb_id
Restrições: nullable=False, unique=True

**7.** Abra `models/filme_favorito.py`. O que o método `@classmethod adicionar` faz passo a passo? O que acontece se o filme já existir nos favoritos?
Método: adicionar()
Passos:
Verifica se o filme já existe usando buscar_por_tmdb().
Se existir, retorna None.
Cria um objeto FilmeFavorito.
Adiciona ao banco com db.session.add().
Executa db.session.commit().
Retorna o favorito criado.

Se o filme já existir nos favoritos, nada é salvo.

**8.** Onde está o método que lista as últimas 8 buscas? Qual é o nome da classe e do método?
Está em:
Arquivo: models/historico_busca.py
Classe: HistoricoBusca
Método: ultimas()

**9.** O model grava dados da API TMDB inteira ou só alguns campos espelhados? Cite 4 campos salvos em `FilmeFavorito`.
O model salva apenas alguns campos espelhados da API, não a resposta inteira.
Campos salvos: tmdb_id, titulo, poster_path, nota


**10.** Em `models/__init__.py`, o que é exportado além de `db`? Por que o controller importa `from models import FilmeFavorito` em vez de importar o arquivo inteiro da pasta?
Em models/__init__.py são exportados: db, ModeloBase, FilmeFavorito, HistoricoBusca
porque a classe já foi exportada pelo pacote models.

---

## Bloco B — Controller (perguntas 11 a 20)

**11.** Quantos Blueprints existem no projeto? Cite o **nome** de cada um e o **url_prefix** (se tiver).
Existem 3 Blueprints: dashboard_bp   nenhum
filmes_bp   /filmes
favoritos_bp   /favoritos

**12.** Em qual arquivo está a rota `/filmes/populares`? Qual é o nome da função Python que responde essa URL?
Arquivo: controllers/filmes_controller.py
Função: populares()

**13.** O que a função `populares()` faz antes de chamar `render_template`? Cite duas chamadas (Model, Service ou API).
Antes do render_template() a função: Cria a API: api = TmdbApi()  Busca filmes populares: filmes, demo = api.filmes_populares()

**14.** Quando o usuário busca um filme em `/filmes/buscar`, qual controller registra o termo no banco? Qual model é usado e em qual linha aproximada?
Controller: controllers/filmes_controller.py
Model usado: HistoricoBusca fica aproximadamente no meio da função buscar().

**15.** Abra `controllers/favoritos_controller.py`. Qual método HTTP é exigido para adicionar favorito (`GET` ou `POST`)? Qual a URL completa de exemplo para adicionar o filme id 550?
Método HTTP: POST
Rota: /favoritos/adicionar/550

**16.** No `filmes_controller.py`, rota `detalhe(filme_id)`: o que acontece se `api.detalhe(filme_id)` retornar `None`?
O usuário é redirecionado para: url_for("filmes.populares")

**17.** Onde os Blueprints são **registrados** no Flask? Cite o arquivo e o comando usado (3 registros).
Os Blueprints são registrados em: app.py
Comandos: app.register_blueprint(dashboard_bp)
app.register_blueprint(filmes_bp)
app.register_blueprint(favoritos_bp)

**18.** Qual controller cuida da página inicial `/`? Quais variáveis ele envia para o template `index.html`?
Controller: controllers/dashboard_controller.py
Variáveis enviadas: populares, melhores, total_favoritos, historico, modo_demo

**19.** A pasta `services/tmdb_api.py` é Model, Controller ou View? Justifique: quem chama essa classe e para quê?
services/tmdb_api.py é Controller.
Quem chama: dashboard_controller.py, filmes_controller.py

**20.** No controller de busca, de onde vem o termo digitado quando o usuário usa o formulário da home (`index.html`)? É `request.form` ou `request.args`? Explique a diferença nesse projeto.
O formulário da home usa: method="GET" 
Portanto o termo vem de: request.args
Diferença: request.args → dados da URL (GET)
request.form → dados enviados por formulário POST

---

## Bloco C — View (perguntas 21 a 30)

**21.** Onde ficam os templates HTML? Qual caminho completo da pasta?
Os templates ficam em: views/templates/

**22.** Qual template é a “base” de todas as páginas (layout com menu)? Como os outros templates usam esse layout (qual comando Jinja)?
Template base: views/templates/layout.html
Os outros usam: {% extends "layout.html" %}

**23.** Abra `views/templates/layout.html`. Liste os 5 links do menu e o `url_for` de cada um.
Menu do layout.html: StreamFlix    url_for('dashboard.index')
Populares   url_for('filmes.populares')
Melhores    url_for('filmes.melhores')
Buscar      url_for('filmes.buscar')
Favoritos   url_for('favoritos.listar')

**24.** Qual arquivo HTML exibe a seção **“Onde assistir (Brasil)”**? De onde vem a variável `streaming` usada nessa tela?
Arquivo: views/templates/filmes/detalhe.html
A variável streaming vem do controller

**25.** O arquivo `filmes/_card.html` é uma página inteira ou um pedaço reutilizado? Quem inclui esse arquivo e com qual tag Jinja?
filmes/_card.html é um componente reutilizável
É incluído com: {% include "filmes/_card.html" %}

**26.** Em `filmes/detalhe.html`, como a View sabe se o filme já está nos favoritos? Qual variável booleana/objeto controla o botão “Salvar” vs “Remover”?
A View verifica: {% if favorito %}
A variável: favorito = FilmeFavorito.buscar_por_tmdb(filme_id)

**27.** Onde está o CSS do site? Como o `layout.html` carrega esse arquivo (função Flask/Jinja)?
CSS: views/static/css/style.css
Carregado por: {{ url_for('static', filename='css/style.css') }}

**28.** Na listagem de favoritos (`favoritos/lista.html`), qual loop Jinja percorre os registros? Cite 3 campos exibidos na tabela.
Loop: {% for fav in favoritos %}
Campos exibidos: fav.titulo, fav.nota, fav.ano

**29.** O que significa `{% if modo_demo %}` no layout? Quem disponibiliza essa variável para **todos** os templates?
Significa: "Se o sistema estiver rodando em modo demonstração".
A variável é disponibilizada para todos os templates em: app.py

**30.** Desenhe ou descreva o fluxo completo quando o aluno clica em **“Salvar favorito”** no detalhe do filme, indicando **View → Controller → Model** (e redirect de volta). Cite arquivos envolvidos.
Fluxo ao clicar em Salvar favorito:

View
Arquivo: views/templates/filmes/detalhe.html

Controller
Arquivo: controllers/favoritos_controller.py

Model
Arquivo: models/filme_favorito.py
---

## Entrega

- Arquivo `.txt` ou `.md` com as 30 respostas 

**Critério:** respostas que mostrem que você **abriu o código**, não chute.

Boa exploração!
