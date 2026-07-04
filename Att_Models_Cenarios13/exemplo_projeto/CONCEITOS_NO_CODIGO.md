# Onde estão os comentários no código?

Os alunos devem ler estes arquivos na ordem:

1. `models/__init__.py` — import com **ponto** (.) vs sem ponto
2. `models/base.py` — `__abstract__ = True`
3. `models/cliente.py` — `@classmethod` e `self`
4. `models/pedido.py` — `@property` (total, subtotal)
5. `controllers/clientes_controller.py` — **Blueprint** + `@route`
6. `app.py` — `register_blueprint` (ligar os módulos)
7. `views/templates/layout.html` — `url_for('blueprint.funcao')`
8. `views/templates/pedidos/detalhe.html` — `@property` no Jinja

Resumo: **Blueprint = pacote de rotas**, **register_blueprint = plugar no app**, **url_for('clientes.listar') = apelido + função**.
