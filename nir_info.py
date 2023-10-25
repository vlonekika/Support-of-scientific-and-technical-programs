from PyQt5.QtWidgets import QStyledItemDelegate
from info_form import Info_Form
from nir_buttons import AddButton, EditButton, FilterButton
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QTableWidgetSelectionRange, QAbstractItemView, QDialog

class ZeroPaddedDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        # Преобразование числа в строку с ведущими нулями (4 символа)
        return f"{int(value):04d}"

class Nir_Info(Info_Form):

    def __init__(self):

        self.__db = "SUBDlab.db"
        self.__tb_name = "ntp_proj"
        self.request = f"""SELECT   "Программа", 
                                    codprog AS "код НТП",
                                    fixed_f AS "номер  пр.",
	                                codtype AS "хар. пр.",
	                                codisp AS "код орг.",
	                                grnti AS "код ГРНТИ",
	                                pfin AS "план. фин. на год",
                                    ffin AS "факт. фин. тек. года",
                                    isp AS "орг. исп.",
                                    srok_n AS "нач. вып.",
                                    srok_k AS "кон. вып.",
                                    ruk AS "рук.",
                                    ruk2 AS "долж.",
                                    nir AS "наим. проекта",
                                    pfin1 AS "план. фин. кв. 1",
                                    pfin2 AS "план. фин. кв. 2",
                                    pfin3 AS "план. фин. кв. 3",
                                    pfin4 AS "план. фин. кв. 4",
                                    ffin1 AS "факт. фин. кв. 1",
                                    ffin2 AS "факт. фин. кв. 2",
                                    ffin3 AS "факт. фин. кв. 3",
                                    ffin4 AS "факт. фин. кв. 4" 
                            FROM (SELECT ntp_prog.prog AS "Программа", ntp_proj.* 
                            FROM ntp_proj
                            JOIN ntp_prog ON ntp_proj.codprog = ntp_prog.codprog)"""
        self.order = 'ORDER BY   "код НТП", "номер  проекта"'
        super().__init__(self.__db, self.__tb_name, self.request + self.order)

        self.state = None
        self.table.setItemDelegateForColumn(2, ZeroPaddedDelegate())
        self.selected_row = None
        self.table.itemSelectionChanged.connect(self.selection_changed)

        headers = []
        for col in range(self.table.columnCount()):
            header_item = self.table.horizontalHeaderItem(col)
            if header_item:
                headers.append(header_item.text())
            else:
                headers.append(col)
        self.sort_com.addItems(["Код НТП + номер проекта"] + headers)

        self.setup_size()

        self.add.clicked.connect(self.add_button)
        self.edit.clicked.connect(self.edit_button)
        self.delet.clicked.connect(self.delete_button)
        self.filter.clicked.connect(self.filter_button)
        self.sort.clicked.connect(self.sort_button)

    def add_button(self):
        add_button = AddButton()
        result = add_button.exec_()

        self.table.clearContents()
        self.table.setRowCount(0)
        self.db_load(self.__db, self.__tb_name, self.request + self.order)
        if result == QDialog.Accepted:
            value_1, value_2 = add_button.get_row()
            row = self.search(value_1, value_2)
            self.table.clearSelection()
            selection_range = QTableWidgetSelectionRange(row, 0, row, self.table.columnCount() - 1)
            self.table.setRangeSelected(selection_range, True)
            self.table.scrollToItem(self.table.item(row, 0), QAbstractItemView.PositionAtTop)
            self.update_ntp_prog()
        self.setup_size()

    def edit_button(self):
        if self.selected_row not in (-1, None):
            codprog = self.table.item(self.selected_row, 1)
            f = self.table.item(self.selected_row, 2)
            if codprog and f and self.show_warning("Вы уверены, что хотите редактировать запись?") == QtWidgets.QMessageBox.Yes:

                codprog = codprog.text()
                f = f.text()
                db = QSqlDatabase.addDatabase('QSQLITE')
                db.setDatabaseName(self.__db)
                db.open()
                request = f"""SELECT codprog, fixed_f,  nir, isp, srok_n, srok_k, ruk, ruk2, grnti, codtype, pfin FROM Ntp_proj
                                             WHERE codprog = {int(codprog)} AND f = {int(f)};"""
                query = QSqlQuery(request)
                while query.next():
                    codprog = query.value(0)
                    val = QSqlQuery(f"SELECT prog FROM Ntp_prog WHERE codprog = {codprog}")
                    while val.next():
                        codprog = val.value(0)
                    fixed_f = query.value(1)
                    nir = query.value(2)
                    isp = query.value(3)
                    srok_n = query.value(4)
                    srok_k = query.value(5)
                    ruk = query.value(6)
                    ruk2 = query.value(7)
                    grnti = query.value(8)
                    codtype = query.value(9)
                    pfin = query.value(10)
                db.close()
                edit_button = EditButton(codprog, fixed_f,  nir, isp, srok_n, srok_k, ruk, ruk2, grnti, codtype, pfin)
                result = edit_button.exec_()
                if result == QDialog.Accepted:
                    self.table.clearContents()
                    self.table.setRowCount(0)
                    self.db_load(self.__db, self.__tb_name, self.request + self.order)
                    value_1, value_2 = edit_button.get_row()
                    row = self.search(value_1, value_2)
                    self.table.clearSelection()
                    selection_range = QTableWidgetSelectionRange(row, 0, row, self.table.columnCount() - 1)
                    self.table.setRangeSelected(selection_range, True)
                    self.table.scrollToItem(self.table.item(row, 0), QAbstractItemView.PositionAtTop)
                    self.update_ntp_prog()
                self.setup_size()

    def delete_button(self):
        if self.selected_row not in (-1, None):
            codprog = self.table.item(self.selected_row, 1)
            f = self.table.item(self.selected_row, 2)
            if codprog and f:
                if self.show_warning("Вы уверены, что хотите удалить запись?") == QtWidgets.QMessageBox.Yes:
                    codprog = codprog.text()
                    f = f.text()
                    db = QSqlDatabase.addDatabase('QSQLITE')
                    db.setDatabaseName(self.__db)
                    db.open()
                    query = QSqlQuery()
                    request = f"""DELETE FROM Ntp_proj
                                     WHERE codprog = {int(codprog)} AND f = {int(f)};"""
                    query.prepare(request)
                    query.exec_()
                    db.close()

                    self.table.clearContents()
                    self.table.setRowCount(0)
                    self.db_load(self.__db, self.__tb_name, self.request + self.order)
                    self.update_ntp_prog()
                    self.setup_size()

    def filter_button(self):
        filter_button = FilterButton(self.state)
        result = filter_button.exec_()
        self.state = filter_button.get_state()
        vuz_lst, codprog = filter_button.set_filter_button()
        if result == QDialog.Accepted:
            if codprog != "Все" and len(vuz_lst) != 1:
                line = f'WHERE "Программа" = "{codprog}" AND "орг. исп." IN {vuz_lst}'
                self.table.clearContents()
                self.table.setRowCount(0)
                self.db_load(self.__db, self.__tb_name, self.request + line + self.order)
            elif codprog == "Все" and len(vuz_lst) != 1:
                line = f'WHERE "орг. исп." IN {vuz_lst}'
                self.table.clearContents()
                self.table.setRowCount(0)
                self.db_load(self.__db, self.__tb_name, self.request + line + self.order)
            elif codprog == "Все" and len(vuz_lst) == 1:
                line = f'WHERE "орг. исп." = "{vuz_lst[0]}"'
                self.table.clearContents()
                self.table.setRowCount(0)
                self.db_load(self.__db, self.__tb_name, self.request + line + self.order)
            elif codprog != "Все" and len(vuz_lst) == 1:
                line = f'WHERE "Программа" = "{codprog}" AND "орг. исп." == "{vuz_lst[0]}"'
                self.table.clearContents()
                self.table.setRowCount(0)
                self.db_load(self.__db, self.__tb_name, self.request + line + self.order)
            self.setup_size()

    def sort_button(self):
        lst = ["Код НТП + номер проекта", "Программа", 'код НТП', 'номер  пр.', 'хар. пр.', 'код орг.', 'код ГРНТИ',
         'план. фин. на год', 'факт. фин. тек. года', 'орг. исп.', 'нач. вып.',
         'кон. вып.', 'рук.', 'долж.', 'наим. проекта', 'план. фин. кв. 1',
         'план. фин. кв. 2', 'план. фин. кв. 3', 'план. фин. кв. 4', 'факт. фин. кв. 1', 'факт. фин. кв. 2',
         'факт. фин. кв. 3', 'факт. фин. кв. 4']
        if self.sort_com.currentText() == lst[0]:
            res = self.request + 'ORDER BY   "код НТП", "номер  проекта"'
        else:
            res = self.request + f'ORDER BY  "{lst[lst.index(self.sort_com.currentText())]}"'

        self.table.clearContents()
        self.table.setRowCount(0)

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.__db)
        db.open()

        query = QSqlQuery(res)
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
        self.setup_size()

    def update_ntp_prog(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.__db)
        db.open()
        query = QSqlQuery()
        request = f"""UPDATE Ntp_prog AS prog
                      SET nproj = (SELECT COUNT(codprog) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog),
                      pfin = COALESCE((SELECT SUM(pfin) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      pfin1 = COALESCE((SELECT SUM(pfin1) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      pfin2 = COALESCE((SELECT SUM(pfin2) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      pfin3 = COALESCE((SELECT SUM(pfin3) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      pfin4 = COALESCE((SELECT SUM(pfin4) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      ffin = COALESCE((SELECT SUM(ffin) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      ffin1 = COALESCE((SELECT SUM(ffin1) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      ffin2 = COALESCE((SELECT SUM(ffin2) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      ffin3 = COALESCE((SELECT SUM(ffin3) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0),
                      ffin4 = COALESCE((SELECT SUM(ffin4) FROM Ntp_proj AS proj WHERE proj.codprog = prog.codprog), 0);
                   """
        query.prepare(request)
        query.exec_()
        db.close()

    def show_warning(self, warning):

        """Вывод предупреждения о пользовательской ошибке
            args:
            warning - предупреждениe"""

        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Question)
        msg_box.setText(warning)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
        msg_box.button(QtWidgets.QMessageBox.Yes).setText("Да, выполнить")
        msg_box.button(QtWidgets.QMessageBox.No).setText("Нет, отменить")
        return msg_box.exec_()

    def selection_changed(self):
        selected_rows = self.table.selectionModel().selectedRows()
        self.selected_row = selected_rows[0].row() if selected_rows else -1

    def setup_size(self):
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(5, 90)
        self.table.setColumnWidth(8, 90)
        self.table.setColumnWidth(11, 150)
        self.table.setColumnWidth(12, 150)
        self.table.setColumnWidth(13, 250)

    def search(self, value_1, value_2):
        for row in range(self.table.rowCount()):
            item1 = self.table.item(row, 1)
            item2 = self.table.item(row, 2)

            if item1 is not None and item2 is not None:
                if item1.text() == value_1 and item2.text() == value_2:
                    return row

        return None
