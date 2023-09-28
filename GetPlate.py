import tkinter as tk
from tkinter import messagebox
from GetConnection import conexao
from datetime import *
import json
from plyer import notification
import pyperclip
import os
import ImageCreatedHandler as ich
from manipularhtml import *
from manipularhtml import tratarHtmlResponse


def show_popup(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=5  # Exibe o popup por 5 segundos
    )


# Acesso ao arquivo JSON para pegar as informações do veículo e a placa

def getP():
    data_e_hora_atuais = datetime.now()
    dataHora = data_e_hora_atuais.strftime("%Y-%m-%d %H-%M-%S.%f")

    with open('data.json', 'r', encoding='utf8') as f:
        dados = json.load(f)
        openalpr_results = dados.get("results")
        try:
            quantidade_placas = len(openalpr_results)

            resultado = {}
            info_geral = {}

            if quantidade_placas == None or quantidade_placas < 1:
                print("Nenhuma Placa identificada...")

            else:
                for x in range(quantidade_placas):
                    placa = openalpr_results[x]["plate"]
                    openalpr_veiculo = openalpr_results[x]["vehicle"]
                    cor = openalpr_veiculo['color']
                    fabricante = openalpr_veiculo['make']
                    tipo = openalpr_veiculo['body_type']
                    ano = openalpr_veiculo['year']
                    modelo = openalpr_veiculo['make_model']

                    info_geral['Placa'] = placa
                    info_geral['Cor'] = cor[0]['name']
                    info_geral['Fabricante'] = fabricante[0]['name']
                    info_geral['Tipo'] = tipo[0]['name']
                    info_geral['Ano'] = ano[0]['name']
                    info_geral['Modelo'] = modelo[0]['name']

                    data = datetime.now()
                    cor2 = cor[0]['name']
                    fabricante2 = fabricante[0]['name']
                    tipo2 = tipo[0]['name']
                    ano2 = ano[0]['name']
                    modelo2 = modelo[0]['name']

                    resultado['Veiculo {}'.format(x + 1)] = info_geral
                    info_geral = {}
                    print("Placa Obtida: "+placa)
                    if len(placa) != 7:
                        print('Não é uma placa válida!')
                    else:
                        tratarHtmlResponse(placa)

                        # Verifica se a placa do veiculo já existe no banco
                        conexao.connect()
                        cursor = conexao.cursor()
                        sql = f'SELECT * FROM veiculos WHERE veiculos.placa = "{placa}"'
                        cursor.execute(sql)
                        result = cursor.fetchone()

                        if result != None:
                            print(result)
                            print("Já existe a Placa " + placa +
                                  " no banco de dados!")
                        else:
                            print(resultado)
                            print("Registrando a placa " +
                                  placa+" no banco de dados!")
                            create = f'INSERT INTO veiculos (data, placa, cor, fabricante, tipo, ano, modelo) VALUES ("{data}","{placa}","{cor2}","{fabricante2}","{tipo2}","{ano2}","{modelo2}")'
                            cursor.execute(create)
                            conexao.commit()
                        cursor.close()
                        conexao.close()

                        # print(resultado)
                        # print(resultado['Veiculo 1'])
                        open('dicionario.json', 'w').write(
                            json.dumps(resultado))
                        show_popup("Monitoramento Portaria",
                                   "Placa Obtida: "+placa)
                        pyperclip.copy(placa)

        except TypeError as error:
            quantidade_placas = 0
            print(f"{dataHora} , {error}\n")
