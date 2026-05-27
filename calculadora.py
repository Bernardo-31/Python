import requests
from flask import Flask, render_template, request
import math

def calcular():
    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]


    if operacao == "sqrt":
        if num1 < 0:
            resultado = "Erro: número negativo"
            etapas = f"Não existe raiz real de {num1}."
        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"
    else:
        num2_valor = request.form.get("num2", "").strip()
        if not num2_valor:
            return render_template(
                "calculadora.html",
                etapas="Informe o segundo número para esta operação.",
                resultados="",
            )
        num2 = float(num2_valor)


        if operacao == "+":
            resultado = num1 + num2
            etapas = f"{num1} + {num2} = {resultado}"

        elif operacao == '-':
            resultado = num1 - num2
            etapas = f'{num1} - {num2} = {resultado}'
    
        elif operacao == '*':
            resultado = num1 * num2
            etapas = f'{num1} * {num2} = {resultado}'

        elif operacao == '/':
            resultado = num1 / num2
            etapas = f'{num1} / {num2} = {resultado}'

        elif operacao == '**':
            resultado = num1 ** num2
            etapas = f'{num1} ** {num2} = {resultado}'

            if num1 == 0  or num2 == 0:
                resultado = "Operacao invalida"
            else :
                print("")
        else:
            resultado = "Operacao invalida"
            etapas = "A operacao selecionada esta ivalida"
            return render_template('calculadora.html') (etapas = etapas, resultado = resultado)
        
    if operacao == "sqrt":
        if num1 < 0:
            resultado = "Erro: numero negativo"
            etapas = f"Nao existe raiz real de {num1}"
        else:
            resultado = math.sqrt(num1)


