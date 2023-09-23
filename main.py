import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUiType
from nir_info import Nir_Info
from ntp_info import Ntp_Info
from vuz_info import Vuz_Info

Ui_BaseForm, QMainWindowBase = loadUiType('menubar.ui')

class BaseForm(QMainWindow, Ui_BaseForm):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        #переход на формы
        self.nir_info.triggered.connect(self.open_nir_info)
        self.ntp_info.triggered.connect(self.open_ntp_info)
        self.vuz_info.triggered.connect(self.open_vuz_info)

        #стэк форм
        self.stacked_widget = QStackedWidget(self)

        #пустое поле в начале
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(central_widget)
        line = """  Все должно быть простым, насколько возможно, но нe проще.\
                    \n\n\t\t\t Приписывается Альберту Эйнштейну"""
        self.main_label = QLabel(line, self)
        self.main_label.setAlignment(Qt.AlignCenter)

        self.ntp_proj_table = Nir_Info()
        self.ntp_prog_table = Ntp_Info()
        self.vuz_table = Vuz_Info()

        self.stacked_widget.addWidget(self.main_label)
        self.stacked_widget.addWidget(self.ntp_proj_table)
        self.stacked_widget.addWidget(self.ntp_prog_table)
        self.stacked_widget.addWidget(self.vuz_table)

    def open_nir_info(self):
        self.stacked_widget.setCurrentWidget(self.ntp_proj_table)

    def open_ntp_info(self):
        self.stacked_widget.setCurrentWidget(self.ntp_prog_table)

    def open_vuz_info(self):
        self.stacked_widget.setCurrentWidget(self.vuz_table)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BaseForm()
    window.show()
    sys.exit(app.exec_())