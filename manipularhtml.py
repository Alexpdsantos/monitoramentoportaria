import requests
from bs4 import BeautifulSoup
import json
from GetPlate import *


def tratarHtmlResponse(placa):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = 'https://www.keplaca.com/placa/'+placa
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            td_elements = soup.find('table')
            h2_elements = soup.find('h2')
            # Pegar cada elemento da tabela obtida do site e armazenar no arquivo datahtml.json
            td_data = []
            for td in td_elements:
                td_data.append(td.text)

            h2 = h2_elements.text.split()
            h2_tratado = h2[2]
            td_dict = {}
            for item in td_data:
                if ":" in item:
                    key, value = item.split(":")
                    td_dict[key.strip()] = value.strip()
            with open('datahtml.json', 'w', encoding='utf-8') as f:
                json.dump(td_dict, f, ensure_ascii=False, indent=2)

            # Ler o arquivo datahtml.json e pegar o valor da chave Segmento
            with open('datahtml.json', 'r', encoding='utf8') as fs:
                dados = json.load(fs)
                segmento = dados.get("Segmento")
        else:
            print('Falha ao obter o modelo do veículo...', response.status_code)
    except requests.Timeout:
        print('Tempo de resposta excedido...')
    except requests.RequestException as e:
        print('Erro na requisição:', str(e))
