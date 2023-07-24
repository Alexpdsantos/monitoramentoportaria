import time
from watchdog.observers import Observer
from watchdog. events import FileSystemEventHandler
from GetPlate import getP
from GetConnection import *

import requests
import json
import base64
from ImageCreatedHandler import *

global imagem


class ImageCreatedHandler(FileSystemEventHandler):
    def __init__(self, function):
        super().__init__()
        self.function = function

    def on_created(self, event):
        if not event.is_directory and (event.src_path.endswith('.jpg') or event.src_path.endswith(".png")):
            self.function(event.src_path)


def ImageHandler():
    path = 'output'
    event_handler = ImageCreatedHandler(process_image)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def process_image(path):
    global imagem
    caminho_absoluto = f'{path}'
    caminho = caminho_absoluto.split('\\')
    imagem = caminho_absoluto
    print(f"--------------------\n {caminho[1]}...")
    time.sleep(2)
    getVehicle()


# Acesso à API OpenAlpr e processamento de imagem para obter e gravar as informações do veículo em arquivo JSON
def getVehicle():
    try:
        with open(imagem, "rb") as image_file:
            img_base64 = base64.b64encode(image_file.read())

        url = 'https://api.openalpr.com/v3/recognize_bytes?recognize_vehicle=1&country=br&secret_key=%s' % (
            SECRET_KEY)
        r = requests.post(url, data=img_base64)

        # Salvar arquivo JSON
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(r.json(), f, ensure_ascii=False, indent=2)

        getP()
    except FileNotFoundError as ex:
        print(f'Arquivo não encontrado!{ex}')
        return
    except Exception as exception:
        print(f"Exceção não tratada!{exception}")


# IMAGE_PATH = imagem
