import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import cv2
import numpy as np
from datetime import datetime
import threading
from GetConnection import *
from configs import *
from ImageCreatedHandler import *

thread = threading.Thread(target=ImageHandler)
thread.daemon = True
thread.start()

class VideoWindow(QMainWindow):
    def __init__(self, source, pos_linha, offset, largura_min, altura_min):
        super().__init__()

        self.setWindowTitle("Monitoramento")
        self.setGeometry(100, 100, 980, 600)

        # Configurar o layout
        layout = QVBoxLayout()

        # Criar um QLabel para exibir o vídeo
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # Iniciar o thread para a captura de vídeo
        self.capture_thread = threading.Thread(
            target=self.start_camera,
            args=(source, pos_linha, offset, largura_min, altura_min)
        )
        self.capture_thread.daemon = True
        self.capture_thread.start()

        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(layout)

    def start_camera(self, source, pos_linha, offset, largura_min, altura_min):
        cap = cv2.VideoCapture(source)
        subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()
        detec = []
        ret = True
        while ret:
            ret, frame = cap.read()
            ret, frame2 = cap.read()
            grey = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(grey, (3, 3), 5)
            img_sub = subtracao.apply(blur)
            dilat = cv2.dilate(img_sub, np.ones((5, 5)))
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
            dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
            contorno, img = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cv2.line(frame2, (0, pos_linha), (1920, pos_linha), (255, 127, 0), 1)

            # Desenhar os contornos em cada objeto detectado
            for (i, c) in enumerate(contorno):
                (x, y, w, h) = cv2.boundingRect(c)
                validar_contorno = (w >= largura_min) and (h >= altura_min)
                if not validar_contorno:
                    continue
                cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 1)
                centro = self.get_center(x, y, w, h)
                detec.append(centro)
                cv2.circle(frame2, centro, 1, (255, 255, 255), 1)

            # Processar detecções
            for (x, y) in detec:
                if (pos_linha + offset) > y > (pos_linha - offset):
                    data_e_hora_atuais = datetime.now()
                    dataHora = data_e_hora_atuais.strftime("%Y-%m-%d %H-%M-%S.%f")
                    #carros += 1
                    cv2.imwrite("output/img" + dataHora + ".jpg", frame)
                    cv2.line(frame2, (0, pos_linha), (1920, pos_linha), (0, 127, 255), 1)
                    detec.remove((x, y))

            frame = cv2.resize(frame, (980, 600))
            frame2 = cv2.resize(frame2, (980, 600))

            # Converter o frame OpenCV para um formato exibível no QLabel
            qt_image = self.convert_frame_to_qimage(frame2)
            pixmap = QPixmap.fromImage(qt_image)

            # Atualizar o QLabel com o novo frame
            self.label.setPixmap(pixmap)

            ch = cv2.waitKey(1)
            if ch == ord('q') or ch == ord('Q'):
                """data_e_hora_atuais2 = datetime.now()
                dataHora2 = data_e_hora_atuais2.strftime("%Y-%m-%d %H-%M-%S.%f")
                cv2.imwrite("output/img" + dataHora2 + ".jpg", frame)"""

                self.save_image(frame)

            if ch == 27:
                print("Fechando o Vídeo...")
                break

        cv2.destroyAllWindows()
        cap.release()

    def get_center(self, x, y, largura, altura):
        x1 = largura // 2
        y1 = altura // 2
        cx = x + x1
        cy = y + y1
        return cx, cy
        

    def convert_frame_to_qimage(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qt_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        return qt_image.rgbSwapped()
    
    def save_image(self, frame):
        data_e_hora_atuais = datetime.now()
        dataHora = data_e_hora_atuais.strftime("%Y-%m-%d %H-%M-%S.%f")
        cv2.imwrite("output/img" + dataHora + ".jpg", frame)

def run(source, pos_linha, offset, largura_min, altura_min):

    # Crie a janela de vídeo
    video_window = VideoWindow(source, pos_linha, offset, largura_min, altura_min)
    video_window.show()