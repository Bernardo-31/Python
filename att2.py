from flask import Flask

app = Flask(__name__)

@app.route('/decorator') 
def decoratorex():
    return '''   <!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Currículo - [Seu Nome]</title>
    <style>
        body { font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; background-color: #f4f4f9; }
        .container { max-width: 800px; margin: auto; background: #fff; padding: 40px; box-shadow: 0 0 10px rgba(0,0,0,0.1); border-radius: 8px; }
        h1 { color: #2c3e50; margin-bottom: 5px; }
        h2 { color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; margin-top: 25px; }
        .header { text-align: center; margin-bottom: 30px; }
        .contact-info { color: #7f8c8d; font-size: 0.9em; }
        .job-title { font-size: 1.2em; color: #3498db; font-weight: bold; }
        .item { margin-bottom: 20px; }
        .item-header { display: flex; justify-content: space-between; font-weight: bold; }
        .date { color: #7f8c8d; font-style: italic; }
        ul { padding-left: 20px; }
        @media (max-width: 600px) { .container { padding: 20px; } }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>[Seu Nome Completo]</h1>
        <p class="job-title">[Sua Profissão / Área de Atuação]</p>
        <p class="contact-info">
            [Telefone] | [Email] | [Cidade, Estado] | 
            <a href="[Link LinkedIn]" target="_blank">LinkedIn</a>
        </p>
    </div>

    <section>
        <h2>Resumo Profissional</h2>
        <p>[Escreva um breve parágrafo resumindo sua experiência, habilidades principais e o que você busca na carreira profissional.]</p>
    </section>

    <section>
        <h2>Experiência Profissional</h2>
        
        <div class="item">
            <div class="item-header">
                <span>[Nome da Empresa] - [Cargo]</span>
                <span class="date">[Mês/Ano] - Atual</span>
            </div>
            <ul>
                <li>[Realização ou responsabilidade principal 1]</li>
                <li>[Realização ou responsabilidade principal 2]</li>
            </ul>
        </div>

        <div class="item">
            <div class="item-header">
                <span>[Nome da Empresa] - [Cargo]</span>
                <span class="date">[Mês/Ano] - [Mês/Ano]</span>
            </div>
            <ul>
                <li>[Realização ou responsabilidade principal 1]</li>
            </ul>
        </div>
    </section>

    <section>
        <h2>Educação</h2>
        <div class="item">
            <div class="item-header">
                <span>[Nome da Instituição] - [Nome do Curso]</span>
                <span class="date">[Ano de Início] - [Ano de Conclusão]</span>
            </div>
        </div>
    </section>

    <section>
        <h2>Habilidades</h2>
        <p>[Habilidade 1], [Habilidade 2], [Habilidade 3], [Habilidade 4]</p>
    </section>
</div>

</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True) 