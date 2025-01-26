import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from design import Ui_MainWindow, QtWidgets
from sc import *


def resize(image):
    return cv2.resize(image, (500, 500), interpolation=cv2.INTER_AREA)

DATA = []
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_load.clicked.connect(self.load_file)
        self.ui.pushButton_save.clicked.connect(self.save_file)

    def load_file(self):
        global DATA
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл", "", "*.jpg")
        self.ui.label_path.setText(file_path)
        callback = load_image(file_path)

        DATA += [callback]
        try:
            image = callback[-1]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = resize(image)
            height, width, channels = image.shape
            bytes = channels * width

            qimage = QImage(image.data, width, height, bytes, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.ui.frame.setPixmap(pixmap)
            self.ui.frame.setScaledContents(True)

        except Exception as e:
            print(e)

    def save_file(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку", "")
        try:
            save_results(DATA, directory)
        except Exception as e:
            self.ui.label_path.setText('Wrong directory')
            print(e)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

'''
self.label.setFrameShape(QtWidgets.QFrame.Box)
self.label.setFrameShadow(QtWidgets.QFrame.Plain)
self.label.setAlignment(QtCore.Qt.AlignCenter)
'''