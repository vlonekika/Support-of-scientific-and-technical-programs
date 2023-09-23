from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUiType
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


Ui_Info_Form, QInfo_Form = loadUiType('info_form.ui')

class Info_Form(QMainWindow, Ui_Info_Form):

    def __init__(self, db_name, tb_name, request):
        super().__init__()
        self.setupUi(self) # установка интерфейса
        self.db_load(db_name, tb_name, request) #загрузка БД


    def db_load(self, db_name: str, tb_name: str, request:str, *args, **kwargs):
        """ Функция заполнения таблицы НТП проектов.
            args:
            db_name:str - название БД
            tb_name:str - название таблицы
            request:str - запрос"""

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_name)
        db.open()

        query = QSqlQuery(request)
        column_count = query.record().count()
        self.table.setColumnCount(column_count)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for col in range(column_count):
            header_item = QTableWidgetItem(query.record().fieldName(col))
            self.table.setHorizontalHeaderItem(col, header_item)

        row = 0
        while query.next():
            self.table.setRowCount(row + 1)
            for col in range(column_count):
                item = QTableWidgetItem(str(query.value(col)))
                self.table.setItem(row, col, item)
            row += 1

        db.close()
