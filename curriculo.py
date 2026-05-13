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
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .cv-container {
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        header {
            text-align: center;
            border-bottom: 2px solid #35424a;
            padding-bottom: 20px;
            margin-bottom: 20px;
        }
        header h1 {
            margin: 0;
            color: #35424a;
            text-transform: uppercase;
        }
        header p {
            margin: 5px 0;
            color: #555;
        }
        h2 {
            color: #35424a;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
            margin-top: 25px;
        }
        .item {
            margin-bottom: 15px;
        }
        .item-header {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
        }
        .date {
            color: #777;
            font-style: italic;
        }
        ul {
            margin-top: 5px;
        }
        .skills {
            display: flex;
            justify-content: space-between;
        }
        .skill-box {
            width: 45%;
        }
    </style>
</head>
<body>

<div class="cv-container">
    <header>
        <h1>[Seu Nome Completo]</h1>
        <p>[Sua Profissão/Área]</p>
        <p>Telefone: (00) 99999-9999 | E-mail: seu.email@email.com</p>
        <p>LinkedIn: ://linkedin.com | Cidade - Estado</p>
    </header>

    <section>
        <h2>Resumo Profissional</h2>
        <p>[Escreva um breve resumo sobre você, sua experiência e seus objetivos profissionais (2-3 linhas).]</p>
    </section>

    <section>
        <h2>Experiência de Trabalho</h2>
        
        <div class="item">
            <div class="item-header">
                <span>[Nome da Empresa] - [Cargo]</span>
                <span class="date">[Mês/Ano] – [Mês/Ano ou Atual]</span>
            </div>
            <ul>
                <li>[Realização ou responsabilidade 1]</li>
                <li>[Realização ou responsabilidade 2]</li>
            </ul>
        </div>

        <div class="item">
            <div class="item-header">
                <span>[Nome da Empresa Anterior] - [Cargo]</span>
                <span class="date">[Mês/Ano] – [Mês/Ano]</span>
            </div>
            <ul>
                <li>[Realização ou responsabilidade 1]</li>
            </ul>
        </div>
    </section>

    <section>
        <h2>Formação Acadêmica</h2>
        <div class="item">
            <div class="item-header">
                <span>[Nome da Instituição] - [Nome do Curso]</span>
                <span class="date">[Ano de Início] – [Ano de Conclusão]</span>
            </div>
        </div>
        <div class="item">
            <div class="item-header">
                <span>[Nome da Instituição 2] - [Nome do Curso 2]</span>
                <span class="date">[Ano de Início] – [Ano de Conclusão]</span>
            </div>
        </div>
    </section>

    <section>
        <h2>Cursos e Certificações</h2>
        <ul>
            <li>[Nome do Curso 1] - [Instituição] ([Ano])</li>
            <li>[Nome do Curso 2] - [Instituição] ([Ano])</li>
        </ul>
    </section>

    <section>
        <h2>Idiomas</h2>
        <div class="skills">
            <div class="skill-box">
                <p><strong>Inglês:</strong> [Nível: Ex. Avançado/Fluente]</p>
            </div>
            <div class="skill-box">
                <p><strong>Espanhol:</strong> [Nível: Ex. Intermediário]</p>
            </div>
        </div>
    </section>

</div>

</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True) 