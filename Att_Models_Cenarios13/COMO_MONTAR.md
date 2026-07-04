# Como montar seu cenário no projeto MVC (Aula 11)

Escolheu o cenário? Siga os passos **na ordem**.

## Passo 1 — Models (pasta `models/`)

Copie da pasta do seu cenário para `flask/Aula11/models/`:

| Cenário | Arquivos para copiar |
|---------|----------------------|
| **A Locadora** | `cliente_locadora.py`, `veiculo.py`, `locacao.py` |
| **B Cinema** | `filme.py`, `sala.py`, `sessao.py` (+ `ingresso.py` opcional) |
| **C Figurinhas** | `colecionador.py`, `figurinha.py`, `oferta.py` |

- `base.py` **já existe** na Aula 11 — não apague.
- Complete os `TODO ALUNO` nos arquivos.
- Atualize `models/__init__.py` com os imports do **seu** cenário (tem um exemplo em cada pasta).

## Passo 2 — Controller (pasta `controllers/`)

1. Copie o `*_controller.py` do cenário para `flask/Aula11/controllers/`
2. Complete os `TODO ALUNO` no controller
3. Registre o Blueprint em `controllers/__init__.py`
4. Registre no `app.py` (veja `app_registro_EXEMPLO.py` do cenário)

## Passo 3 — View (pasta `views/templates/`)

1. Copie a subpasta de templates do cenário para `views/templates/`
   - Ex.: `views/templates/locadora/` ou `cinema/` ou `figurinhas/`
2. Complete os `TODO ALUNO` no HTML (Jinja2)
3. Adicione link no `layout.html`:

```html
<a href="{{ url_for('NOME_DO_BLUEPRINT.index') }}">Seu cenário</a>
```

## Passo 4 — Testar

```powershell
cd flask/Aula11
python app.py
```

Cadastre dados pelo navegador e confira se lista + formulário funcionam.

## Erros comuns

- Esqueceu `db.create_all()` → tabela não existe
- Blueprint não registrado no `app.py` → 404
- Template no caminho errado → TemplateNotFound
- `url_for` com nome errado do Blueprint → BuildError
