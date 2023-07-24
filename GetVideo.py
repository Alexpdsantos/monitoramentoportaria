import sys
from configs import *
from GetConnection import *
from datetime import *
import cv2
import numpy as np
import threading
from ImageCreatedHandler import *

carros = caminhoes = 0
print('Passo 1')


def startCamera():
    def getCenter(x, y, largura, altura):
        """
        :param x: x do objeto
        :param y: y do objeto
        :param largura: largura do objeto
        :param altura: altura do objeto
        :return: tupla que contém as coordenadas do centro de um objeto
        """
        x1 = largura // 2
        y1 = altura // 2
        cx = x + x1
        cy = y + y1
        return cx, cy
    print('Passo 2')

    def setInfo(detec):
        global carros
        for (x, y) in detec:
            if (pos_linha + offset) > y > (pos_linha - offset):
                data_e_hora_atuais = datetime.now()
                dataHora = data_e_hora_atuais.strftime("%Y-%m-%d %H-%M-%S.%f")
                carros += 1
                cv2.imwrite("output/img" + dataHora + ".jpg", frame)
                cv2.line(frame2, (0, pos_linha),
                         (1920, pos_linha), (0, 127, 255), 1)
                detec.remove((x, y))
    print('Passo 3')
    cap = cv2.VideoCapture(source)
    print('Passo 4')
    # Pega o fundo e subtrai do que está se movendo
    subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()
    print('Passo 5...')
    while True:
        try:
            ret, frame = cap.read()
            ret, frame2 = cap.read()
            grey = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(grey, (3, 3), 5)
            img_sub = subtracao.apply(blur)
            dilat = cv2.dilate(img_sub, np.ones((5, 5)))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
            dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
            contorno, img = cv2.findContours(
                dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.line(frame2, (0, pos_linha),
                     (1920, pos_linha), (255, 127, 0), 1)
            for (i, c) in enumerate(contorno):
                (x, y, w, h) = cv2.boundingRect(c)
                validar_contorno = (w >= largura_min) and (h >= altura_min)
                if not validar_contorno:
                    continue
                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 1)
                centro = getCenter(x, y, w, h)
                detec.append(centro)
                cv2.circle(frame2, centro, 1, (255, 255, 255), 1)

            frame = cv2.resize(frame, (980, 600))
            frame2 = cv2.resize(frame2, (980, 600))
            cv2.imshow("Camera", frame)
            # cv2.imshow("Monitoramento", frame2)

            setInfo(detec)

            ch = cv2.waitKey(1)
            if ch == ord('q') or ch == ord('Q'):
                data_e_hora_atuais2 = datetime.now()
                dataHora2 = data_e_hora_atuais2.strftime(
                    "%Y-%m-%d %H-%M-%S.%f")
                cv2.imwrite("output/img" + dataHora2 + ".jpg", frame)

            if ch == 27:
                print("fechando o Vídeo...")
                break
        except Exception as ex:
            print(
                f"{datetime.now()} Erro ao iniciar o video...\n{ex}Reiniciando processo...")
            startCamera()

    cv2.destroyAllWindows()
    cap.release()


thread = threading.Thread(target=ImageHandler)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    import sys
    app = startCamera()
    sys.exit()
