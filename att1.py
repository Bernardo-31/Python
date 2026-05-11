from flask import Flask


app = Flask(__name__) # inicio o flask

@app.route('/') # Isso é o decorator, ele é usado para mapear a função abaixo para a rota '/'
def decoratorex():
    return 'Um decorator em Python é uma ferramenta poderosa que permite alterar ou estender o comportamento de uma função, método ou classe sem precisar modificar o seu código-fonte original!' # Isso é o que será retornado quando a rota '/' for acessada

if __name__ == '__main__':
    app.run(debug=True) # Isso inicia o servidor Flask em modo de depuração, o que é útil para desenvolvimento