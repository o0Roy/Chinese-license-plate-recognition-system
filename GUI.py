

from PyQt5 import QtCore,QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from Recognition import PlateRecognition
import cv2
import sys, os, xlwt
import numpy as np


class Ui_MainWindow(object):

    def __init__(self):
        self.RowLength = 0
        self.Data = [['文件名称', '录入时间', '车牌号码', '车牌类型', '识别耗时', '车牌信息']]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(555, 670)
        MainWindow.setFixedSize(555, 670)  # 设置窗体固定大小
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 10, 511, 491))  #原始图片位置
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 509, 489))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.label_0 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_0.setGeometry(QtCore.QRect(10, 10, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_0.setFont(font)
        self.label_0.setObjectName("label_0")
        self.label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(10, 40, 481, 441))
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignCenter)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents_1 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_1.setGeometry(QtCore.QRect(0, 0, 669, 629))
        self.scrollAreaWidgetContents_1.setObjectName("scrollAreaWidgetContents_1")
        font = QtGui.QFont()
        font.setPointSize(13)
        self.scrollArea_3 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_3.setGeometry(QtCore.QRect(20, 510, 341, 131))
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 339, 129))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 111, 20))  
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 321, 81))
        self.label_3.setObjectName("label_3")
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_3)
        self.scrollArea_4 = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea_4.setGeometry(QtCore.QRect(370, 510, 161, 131))  # 
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 159, 129))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton.setGeometry(QtCore.QRect(20, 90, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_4.setGeometry(QtCore.QRect(10, 10, 111, 70))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.__openimage)  # 设置点击事件
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.ProjectPath = os.getcwd()  # 获取当前工程文件位置

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "中国车牌识别系统"))
        self.label_0.setText(_translate("MainWindow", "原始图片："))
        self.label.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate("MainWindow", "车牌区域："))
        self.label_3.setText(_translate("MainWindow", ""))
        self.pushButton.setText(_translate("MainWindow", "打开图片"))
        self.label_4.setText(_translate("MainWindow", "车牌号：\n \n\n"))

    # 识别
    def __vlpr(self, path):
        PR = PlateRecognition()
        result = PR.VLPR(path)
        return result

    def __show(self, result, FileName):
        # 显示识别到的车牌位置
        size = (int(self.label_3.width()), int(self.label_3.height()))
        shrink = cv2.resize(result['Picture'], size, interpolation=cv2.INTER_AREA)
        shrink = cv2.cvtColor(shrink, cv2.COLOR_BGR2RGB)
        self.QtImg = QtGui.QImage(shrink[:], shrink.shape[1], shrink.shape[0], shrink.shape[1] * 3,
                                  QtGui.QImage.Format_RGB888)
        self.label_3.setPixmap(QtGui.QPixmap.fromImage(self.QtImg))

    def __openimage(self):
        path, filetype = QFileDialog.getOpenFileName(None, "选择文件", self.ProjectPath,
                                                     "JPEG Image (*.jpg);;PNG Image (*.png);;JFIF Image (*.jfif)")  # ;;All Files (*)
        if path == "":  # 未选择文件
            return
        filename = path.split('/')[-1]

        # 尺寸适配
        size = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR).shape
        if size[0] / size[1] > 1.0907:
            w = size[1] * self.label.height() / size[0]
            h = self.label.height()
            jpg = QtGui.QPixmap(path).scaled(w, h)
        elif size[0] / size[1] < 1.0907:
            w = self.label.width()
            h = size[0] * self.label.width() / size[1]
            jpg = QtGui.QPixmap(path).scaled(w, h)
        else:
            jpg = QtGui.QPixmap(path).scaled(self.label.width(), self.label.height())

        self.label.setPixmap(jpg)
        result = self.__vlpr(path)
        if result is not None:
            self.Data.append(
                [filename, result['InputTime'], result['Number'], result['Type'], str(result['UseTime']) + '秒',
                 result['From']])
            self.__show(result, filename)
            _translate = QtCore.QCoreApplication.translate
            self.label_4.setText(_translate("MainWindow", "车牌号：\n" + result['Number'] + "\n" + result['Type'] + "\n"))
            print("文件名：" + filename + " 车牌号：" + result['Number'] + " " + result['Type'] + "")
        else:
            QMessageBox.warning(None, "Error", "无法识别此图像！", QMessageBox.Yes)
            print("文件名：" + filename + "无法识别")



# 重写MainWindow类
class MainWindow(QtWidgets.QMainWindow):

    def closeEvent(self, event):
            event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
