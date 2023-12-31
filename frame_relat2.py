# Form implementation generated from reading ui file 'frame_relat.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from GetConnection import *
import Main_frame
from Main_frame import *
import sys


class Ui_frameRelat(QMainWindow):
    def setupUi(self, frameRelat):
        def actionFindVehicles():
            buscarVeiculos()
        frameRelat.setObjectName("frameRelat")
        frameRelat.resize(840, 371)
        frameRelat.setStyleSheet("background-color: rgb(241, 242, 254);")
        self.centralwidget = QtWidgets.QWidget(frameRelat)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 820, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.setColumnWidth(0, 10)
        self.tableWidget.setColumnWidth(7, 130)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 10, 111, 31))
        self.pushButton.setObjectName("btnBuscarVeiculos")
        self.pushButton.clicked.connect(actionFindVehicles)

        frameRelat.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(frameRelat)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 21))
        self.menubar.setObjectName("menubar")
        frameRelat.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(frameRelat)
        self.statusbar.setObjectName("statusbar")
        frameRelat.setStatusBar(self.statusbar)
        self.retranslateUi(frameRelat)
        QtCore.QMetaObject.connectSlotsByName(frameRelat)

        def buscarVeiculos():
            result = []
            cont = 0

            conexao.connect()
            cursor = conexao.cursor()
            sql = f'SELECT * FROM monitoramento_portaria.veiculos ORDER BY veiculos.id ASC'
            cursor.execute(sql)
            result = cursor.fetchall()
            conexao.close()
            self.tableWidget.setRowCount(len(result))

            for x in result:
                id = x[0]
                data = x[1]
                placa = x[2]
                cor = x[3]
                fabricante = x[4]
                tipo = x[5]
                ano = x[6]
                modelo = x[7]

                self.tableWidget.setItem(
                    cont, 0, QtWidgets.QTableWidgetItem(str(id)))

                self.tableWidget.setItem(cont, 1, QtWidgets.QTableWidgetItem(
                    data.strftime("%d/%m/%Y %H:%M")))
                self.tableWidget.setItem(
                    cont, 2, QtWidgets.QTableWidgetItem(placa))
                self.tableWidget.setItem(
                    cont, 3, QtWidgets.QTableWidgetItem(cor))
                self.tableWidget.setItem(
                    cont, 4, QtWidgets.QTableWidgetItem(fabricante))
                self.tableWidget.setItem(
                    cont, 5, QtWidgets.QTableWidgetItem(tipo))
                self.tableWidget.setItem(
                    cont, 6, QtWidgets.QTableWidgetItem(ano))
                self.tableWidget.setItem(
                    cont, 7, QtWidgets.QTableWidgetItem(modelo))

                cont += 1

    def retranslateUi(self, frameRelat):
        _translate = QtCore.QCoreApplication.translate
        frameRelat.setWindowTitle(_translate(
            "frameRelat", "Relatório de Placas capturadas"))
        frameRelat.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("frameRelat", "Id"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("frameRelat", "Data"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("frameRelat", "Placa"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("frameRelat", "Cor"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("frameRelat", "Fabricante"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("frameRelat", "Tipo"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("frameRelat", "Ano"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("frameRelat", "Modelo"))
        self.pushButton.setText(_translate("frameRelat", "Atualizar Lista"))
