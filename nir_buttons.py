from PyQt5.QtWidgets import QDialog, QTextEdit
from PyQt5.uic import loadUiType
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

Ui_Add_Button, QAdd_Button = loadUiType('add_button_qd.ui')
Ui_Filter_Button, QFilter_Button = loadUiType('filter.ui')

class BaseButton(QDialog, Ui_Add_Button):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.db = "SUBDlab.db"
        self.tb_name = "ntp_prog"

    def show_warning(self, warning):

        """Вывод предупреждения о пользовательской ошибке
            args:
            warning - предупреждениe"""

        QtWidgets.QMessageBox.information(self, 'Предупреждение', warning)

    def accept(self):
        super( BaseButton, self).accept()

    def cancel(self):
        self.reject()

    def validate_transform(self, action, ntp_name, vuz_name, codtype, number_proj, number_ffin, text_ruk,
                           text_dolj, srok_1, srok_2, text_grnti, text_nir_name):
        self.__flag = True

        if ntp_name == ' ':
            self.show_warning("Выберите из списка программу перед сохранением")
            self.__flag = False
        else:
            request = f"""SELECT codprog
                                  FROM Ntp_prog
                                  WHERE prog = '{ntp_name}'
                                  LIMIT 1"""
            codprog = self.db_loads(request)[0]

        if vuz_name == ' ':
            self.__flag = False
            self.show_warning("Выберите из списка вуз исполнитель перед сохранением")
        else:
            request = f"""SELECT codisp
                                  FROM Ntp_proj
                                  WHERE isp = '{vuz_name}'
                                  LIMIT 1"""
            codisp = self.db_loads(request)[0]

        if codtype == ' ':
            self.__flag = False
            self.show_warning("Выберите из списка характер проекта перед сохранением")
        else:
            if codtype == "Фундаментальное исследование": codtype = "Ф"
            if codtype == "Прикладное исследование": codtype = "П"
            if codtype == "Экспериментальная разработка": codtype = "Р"


        try:
            number = int(number_proj)
            if number < 0:
                self.show_warning("Номер проекта должен быть целым неотрицательным числом")
            else:
                number = number
                if action != "Редактировать" and number in self.close_number:
                    self.__flag = False
                    self.show_warning("Запись с таким номером проекта уже существует, выберите другой номер")
                else:
                    number_proj = number
        except ValueError:
            self.__flag = False
            self.show_warning("Номер проекта должен быть целым неотрицательным числом")

        try:
            number = int(number_ffin)
            if number < 0:
                self.show_warning("План финансирования должен быть целым неотрицательным числом")
            else:
                number_ffin = number
                pfin = [number_ffin // 4] * 4
                if (number_ffin % 4) != 0:
                    pfin[-1] = pfin[-1] + (number_ffin % 4)
        except ValueError:
            self.__flag = False
            self.show_warning("План финансирования должен быть целым числом")

        text = text_ruk

        try:
            if (len(text.split()[1]) > 1 and text.split()[1].count('.') > 0 and len(text.split()) == 2) == False:
                self.__flag = False
                self.show_warning("Поле руководитель введено не по шаблону")
            else:
                text_ruk = text
        except IndexError:
            self.__flag = False
            self.show_warning("Поле руководитель введено не по шаблону")

        try:
            srok_1 = int(srok_1)
            srok_2 = int(srok_2)
            if srok_1 < 0 or srok_2 < 0:
                self.show_warning("Сроки выполнения должны быть целыми неотрицательными числами")
            else:
                srok_n, srok_k = srok_1, srok_2
        except ValueError:
            self.__flag = False
            self.show_warning("Сроки выполнения должны быть целыми числами")

        if srok_k < srok_n or len(str(srok_n)) != len(str(srok_n)) != 4:
            self.__flag = False
            self.show_warning("Срок должен состоять из 4 цифр и срок конца должен быть срока начала!")

        text = text_grnti
        try:
            if sum([(el.count(".") == 2 and len(el.split('.')) == 3) for el in text.split(",")]) != len(
                    text.split(",")):
                self.__flag = False
                self.show_warning("Код ГРНТИ введен не по шаблону")
            else:
                text_grnti = text
        except IndexError:
            self.__flag = False
            self.show_warning("Код ГРНТИ введен не по шаблону")

        text = text_nir_name
        if len(text) == 0:
            self.__flag = False
            self.show_warning("Введите название НИР")
        else:
            text_nir_name = text

        if self.__flag == False:
            return
        else:
            self.accept()
            return {"codprog": codprog, "isp": vuz_name, "codisp": codisp, "codtype": codtype,
                    "f": number_proj, "pfin": number_ffin, "pfin1": pfin[0], "pfin2": pfin[1], "pfin3": pfin[2],
                    "pfin4": pfin[3], "ruk": text_ruk, "ruk2": text_dolj, "srok_n": srok_n, "srok_k" :srok_k,
                    "grnti": text_grnti, "nir": text_nir_name, "ffin": 0, "ffin1": 0, "ffin2": 0, "ffin3": 0,
                    "ffin4": 0}

    def db_loads(self, request):

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.db)
        db.open()
        query = QSqlQuery(request)
        column_values = []
        while query.next():
            column_value = query.value(0)
            column_values.append(column_value)
        db.close()
        return column_values



class AddButton(BaseButton):
    def __init__(self):
        super().__init__()

        #self.text_number_proj.setPlaceholderText("X")
        self.text_grnti.setPlaceholderText("XX.XX.XX, XX.XX.XX")
        #self.text_srok_k.setPlaceholderText("XXXX")
        #self.text_srok_n.setPlaceholderText("XXXX")
        #self.text_ruk.setPlaceholderText("Ильин А.А.")
        #self.text_dolj.setPlaceholderText("доцент")
        #self.text_ffin.setPlaceholderText("XXXXXXX")
        #self.text_nir_name.setPlaceholderText("Философия человека и оптимизация ноосферы")

        request_ntp = f"""SELECT prog
                          FROM Ntp_prog"""
        self.ntp_name_combobox.addItems([" "] + self.db_loads(request_ntp))

        request_vuz = f"""SELECT isp
                          FROM Ntp_proj"""
        self.vuz_name_combobox.addItems([" "] + self.db_loads(request_vuz))
        self.codtype_combobox.addItems([" "] + ["Фундаментальное исследование", "Прикладное исследование", "Экспериментальная разработка"])

        self.ntp_name_combobox.currentIndexChanged.connect(self.on_ntp_name_changed)
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.cancel)

    def on_ntp_name_changed(self):
        if self.ntp_name_combobox.currentText() != " ":
            request = f"""SELECT fixed_f
               FROM Ntp_proj
               WHERE codprog == (SELECT codprog FROM Ntp_prog WHERE prog = '{self.ntp_name_combobox.currentText()}' LIMIT 1)"""
            self.close_number = self.db_loads(request)
            self.num_proj.setPlainText(", ".join(str(el) for el in self.close_number))
            self.num_proj.setLineWrapMode(QTextEdit.NoWrap)
            self.num_proj.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            self.num_proj.verticalScrollBar().setMinimumHeight(5)
        else: self.num_proj.setText(" ")

    def save(self):

        ntp_name = self.ntp_name_combobox.currentText()
        vuz_name = self.vuz_name_combobox.currentText()
        codtype = self.codtype_combobox.currentText()
        number_proj = self.text_number_proj.toPlainText()
        number_ffin = self.text_ffin.toPlainText()
        text_ruk = self.text_ruk.toPlainText()
        text_dolj = self.text_dolj.toPlainText()
        srok_1 = self.text_srok_n.toPlainText()
        srok_2 = self.text_srok_k.toPlainText()
        text_grnti = self.text_grnti.toPlainText()
        text_nir_name = self.text_nir_name.toPlainText()
        action = self.validate_transform("Добавить", ntp_name, vuz_name, codtype, number_proj, number_ffin, text_ruk,
                                       text_dolj, srok_1, srok_2, text_grnti, text_nir_name)
        if action is not None:
            json = action
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(self.db)
            db.open()
            query = QSqlQuery()
            request = """INSERT INTO Ntp_proj (codprog, fixed_f, f, nir, isp, codisp, srok_n, srok_k, ruk, ruk2, grnti, codtype, pfin, pfin1, pfin2, pfin3, pfin4, ffin, ffin1, ffin2, ffin3, ffin4) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """
            query.prepare(request)
            self.codprog = str(json["codprog"])
            query.addBindValue(json["codprog"])
            self.f = str(json["f"])
            query.addBindValue(json["f"])
            query.addBindValue(json["f"])
            query.addBindValue(json["nir"])
            query.addBindValue(json["isp"])
            query.addBindValue(json["codisp"])
            query.addBindValue(json["srok_n"])
            query.addBindValue(json["srok_k"])
            query.addBindValue(json["ruk"])
            query.addBindValue(json["ruk2"])
            query.addBindValue(json["grnti"])
            query.addBindValue(json["codtype"])
            query.addBindValue(json["pfin"])
            query.addBindValue(json["pfin1"])
            query.addBindValue(json["pfin2"])
            query.addBindValue(json["pfin3"])
            query.addBindValue(json["pfin4"])
            query.addBindValue(json["ffin"])
            query.addBindValue(json["ffin1"])
            query.addBindValue(json["ffin2"])
            query.addBindValue(json["ffin3"])
            query.addBindValue(json["ffin4"])
            query.exec_()
            db.close()

    def get_row(self):
        return self.codprog, self.f

class EditButton(BaseButton):
    def __init__(self, codprog, fixed_f,  nir, isp, srok_n, srok_k, ruk, ruk2, grnti, codtype, pfin):
        super().__init__()

        self.label.hide()
        self.num_proj.hide()

        self.text_number_proj.setText(str(fixed_f))
        self.text_grnti.setText(grnti)
        self.text_srok_k.setText(str(srok_k))
        self.text_srok_n.setText(str(srok_n))
        self.text_ruk.setText(ruk)
        self.text_dolj.setText(ruk2)
        self.text_ffin.setText(str(pfin))
        self.text_nir_name.setText(nir)


        self.ntp_name_combobox.addItem(codprog)
        self.ntp_name_combobox.setCurrentText(codprog)
        self.text_number_proj.setEnabled(False)
        self.ntp_name_combobox.setEnabled(False)

        request_vuz = f"""SELECT isp
                          FROM Ntp_proj"""
        self.vuz_name_combobox.addItems(self.db_loads(request_vuz))
        self.vuz_name_combobox.setCurrentText(isp)

        self.codtype_combobox.addItems(["Фундаментальное исследование", "Прикладное исследование", "Экспериментальная разработка"])
        if codtype == "Ф": codtype = "Фундаментальное исследование"
        if codtype == "П": codtype = "Прикладное исследование"
        if codtype == "Р": codtype = "Экспериментальная разработка"
        self.codtype_combobox.setCurrentText(codtype)

        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.cancel)

    def save(self):

        ntp_name = self.ntp_name_combobox.currentText()
        vuz_name = self.vuz_name_combobox.currentText()
        codtype = self.codtype_combobox.currentText()
        number_proj = self.text_number_proj.toPlainText()
        number_ffin = self.text_ffin.toPlainText()
        text_ruk = self.text_ruk.toPlainText()
        text_dolj = self.text_dolj.toPlainText()
        srok_1 = self.text_srok_n.toPlainText()
        srok_2 = self.text_srok_k.toPlainText()
        text_grnti = self.text_grnti.toPlainText()
        text_nir_name = self.text_nir_name.toPlainText()
        action = self.validate_transform("Редактировать", ntp_name, vuz_name, codtype, number_proj, number_ffin, text_ruk,
                                       text_dolj, srok_1, srok_2, text_grnti, text_nir_name)
        if action is not None:
            json = action
            self.codprog = str(json["codprog"])
            self.f = str(json["f"])
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(self.db)
            db.open()
            query = QSqlQuery()
            request = f"""UPDATE Ntp_proj SET 
                           nir = '{json["nir"]}',
                           isp = '{json["isp"]}', 
                           codisp = {json["codisp"]}, 
                           srok_n = {json["srok_n"]}, 
                           srok_k = {json["srok_k"]}, 
                           ruk = '{json["ruk"]}', 
                           ruk2 = '{json["ruk2"]}', 
                           grnti = '{json["grnti"]}', 
                           codtype = '{json["codtype"]}', 
                           pfin = {json["pfin"]}, 
                           pfin1 = {json["pfin1"]}, 
                           pfin2 = {json["pfin2"]}, 
                           pfin3 = {json["pfin3"]}, 
                           pfin4 = {json["pfin"]} 
                           WHERE  codprog = {json["codprog"]} and fixed_f = {json["f"]}"""
            query.prepare(request)
            query.exec_()
            db.close()

    def get_row(self):
        return self.codprog, self.f

class FilterButton(QDialog, Ui_Filter_Button):

    def __init__(self, state=None):
        super().__init__()
        self.setupUi(self)

        self.__db = "SUBDlab.db"
        self.al = ['Все']

        self.start_combo()
        self.selected_states = {"codprogBox": 'Все', "regionBox": 'Все',
                                "oblnameBox": 'Все', "cityBox": 'Все', "z2Box": 'Все'} if state is None else state

        self.load_state()

        self.codprogBox.currentIndexChanged.connect(self.codprogBox_changed)
        self.regionBox.currentIndexChanged.connect(self.regionBox_changed)
        self.oblnameBox.currentIndexChanged.connect(self.oblnameBox_changed)
        self.cityBox.currentIndexChanged.connect(self.cityBox_changed)
        self.z2Box.currentIndexChanged.connect(self.z2Box_changed)


        self.cancel.clicked.connect(self.cancel_button)
        self.remove_filter.clicked.connect(self.remove_filter_button)
        self.set_filter.clicked.connect(self.accept)


    def codprogBox_changed(self):
        self.selected_states['codprogBox'] = self.codprogBox.currentText()

    def regionBox_changed(self):
        self.selected_states['regionBox'] = self.regionBox.currentText()

        if self.selected_states['regionBox'] != "Все":
            self.oblnameBox.blockSignals(True)
            self.cityBox.blockSignals(True)
            self.z2Box.blockSignals(True)

            self.oblnameBox.clear()
            request = f"SELECT DISTINCT oblname FROM vuz WHERE region = '{self.selected_states['regionBox']}' ORDER BY oblname"
            self.oblnameBox.addItems(self.al + self.db_loads(request))

            self.cityBox.clear()
            request = f"SELECT DISTINCT city FROM vuz WHERE region = '{self.selected_states['regionBox']}' ORDER BY city"
            self.cityBox.addItems(self.al + self.db_loads(request))

            self.z2Box.clear()
            request = f"SELECT DISTINCT z2 FROM vuz WHERE region = '{self.selected_states['regionBox']}' ORDER BY z2"
            self.z2Box.addItems(self.al + self.db_loads(request))

            self.oblnameBox.blockSignals(False)
            self.cityBox.blockSignals(False)
            self.z2Box.blockSignals(False)


    def oblnameBox_changed(self):
        self.selected_states['oblnameBox'] = self.oblnameBox.currentText()
        if self.selected_states['oblnameBox'] != "Все":

            self.regionBox.blockSignals(True)
            self.cityBox.blockSignals(True)
            self.z2Box.blockSignals(True)

            self.regionBox.clear()
            request = f"SELECT DISTINCT region FROM vuz WHERE oblname = '{self.selected_states['oblnameBox']}' ORDER BY region LIMIT 1"
            self.regionBox.addItems(self.db_loads(request))

            self.cityBox.clear()
            request = f"SELECT DISTINCT city FROM vuz WHERE oblname = '{self.selected_states['oblnameBox']}' ORDER BY city"
            self.cityBox.addItems(self.al + self.db_loads(request))

            self.z2Box.clear()
            request = f"SELECT DISTINCT z2 FROM vuz WHERE oblname = '{self.selected_states['oblnameBox']}' ORDER BY z2"
            self.z2Box.addItems(self.al + self.db_loads(request))

            self.regionBox.blockSignals(False)
            self.cityBox.blockSignals(False)
            self.z2Box.blockSignals(False)

        self.selected_states['regionBox'] = self.regionBox.currentText()


    def cityBox_changed(self):
        self.selected_states['cityBox'] = self.cityBox.currentText()

        if self.selected_states['cityBox'] != "Все":

            self.regionBox.blockSignals(True)
            self.oblnameBox.blockSignals(True)
            self.z2Box.blockSignals(True)

            self.regionBox.clear()
            request = f"SELECT DISTINCT region FROM vuz WHERE city = '{self.selected_states['cityBox']}' ORDER BY region LIMIT 1"
            self.regionBox.addItems(self.db_loads(request))

            self.oblnameBox.clear()
            request = f"SELECT DISTINCT oblname FROM vuz WHERE city = '{self.selected_states['cityBox']}' ORDER BY oblname LIMIT 1"
            self.oblnameBox.addItems(self.db_loads(request))

            self.z2Box.clear()
            request = f"SELECT DISTINCT z2 FROM vuz WHERE city = '{self.selected_states['cityBox']}' ORDER BY z2"
            self.z2Box.addItems(self.al + self.db_loads(request))

            self.regionBox.blockSignals(False)
            self.oblnameBox.blockSignals(False)
            self.z2Box.blockSignals(False)

            self.selected_states['oblnameBox'] = self.oblnameBox.currentText()
            self.selected_states['regionBox'] = self.regionBox.currentText()

    def z2Box_changed(self):
        self.selected_states['z2Box'] = self.z2Box.currentText()
        if self.selected_states['z2Box'] != "Все":

            self.regionBox.blockSignals(True)
            self.oblnameBox.blockSignals(True)
            self.cityBox.blockSignals(True)
            self.z2Box.blockSignals(True)

            self.regionBox.clear()
            request = f"SELECT DISTINCT region FROM vuz WHERE z2 = '{self.selected_states['z2Box']}' ORDER BY region LIMIT 1"
            self.regionBox.addItems(self.db_loads(request))

            self.oblnameBox.clear()
            request = f"SELECT DISTINCT oblname FROM vuz WHERE z2 = '{self.selected_states['z2Box']}' ORDER BY oblname LIMIT 1"
            self.oblnameBox.addItems(self.db_loads(request))

            self.cityBox.clear()
            request = f"SELECT DISTINCT city FROM vuz WHERE z2 = '{self.selected_states['z2Box']}' ORDER BY city LIMIT 1"
            self.cityBox.addItems(self.db_loads(request))

            self.z2Box.clear()
            request = f"SELECT DISTINCT z2 FROM vuz WHERE z2 = '{self.selected_states['z2Box']}' ORDER BY city LIMIT 1"
            self.z2Box.addItems(self.db_loads(request))

            self.regionBox.blockSignals(False)
            self.oblnameBox.blockSignals(False)
            self.cityBox.blockSignals(False)
            self.z2Box.blockSignals(False)

            self.selected_states['cityBox'] = self.cityBox.currentText()
            self.selected_states['oblnameBox'] = self.oblnameBox.currentText()
            self.selected_states['regionBox'] = self.regionBox.currentText()

    def load_state(self):

        self.codprogBox.setCurrentText(self.selected_states["codprogBox"])

        self.regionBox.setCurrentText(self.selected_states["regionBox"])
        self.regionBox_changed()

        self.oblnameBox.setCurrentText(self.selected_states["oblnameBox"])
        self.oblnameBox_changed()

        self.cityBox.setCurrentText(self.selected_states["cityBox"])
        self.cityBox_changed()

        self.z2Box.setCurrentText(self.selected_states["z2Box"])
        self.z2Box_changed()

    def get_state(self):
        return self.selected_states

    def accept(self):
        super(FilterButton, self).accept()

    def cancel_button(self):
        self.reject()

    def start_combo(self):

        self.regionBox.blockSignals(True)
        self.oblnameBox.blockSignals(True)
        self.cityBox.blockSignals(True)
        self.z2Box.blockSignals(True)

        self.codprogBox.clear()
        request = "SELECT DISTINCT prog FROM Ntp_prog ORDER BY prog"
        self.codprogBox.addItems(self.al + self.db_loads(request))

        self.regionBox.clear()
        request = "SELECT DISTINCT region FROM vuz ORDER BY region"
        self.regionBox.addItems(self.al + self.db_loads(request))

        self.oblnameBox.clear()
        request = "SELECT DISTINCT oblname FROM vuz ORDER BY oblname"
        self.oblnameBox.addItems(self.al + self.db_loads(request))

        self.cityBox.clear()
        request = "SELECT DISTINCT city FROM vuz ORDER BY city"
        self.cityBox.addItems(self.al + self.db_loads(request))

        self.z2Box.clear()
        request = "SELECT DISTINCT z2 FROM vuz ORDER BY z2"
        self.z2Box.addItems(self.al + self.db_loads(request))

        self.regionBox.blockSignals(False)
        self.oblnameBox.blockSignals(False)
        self.cityBox.blockSignals(False)
        self.z2Box.blockSignals(False)

    def set_filter_button(self):
        all_values = tuple([self.z2Box.itemText(i) for i in range(self.z2Box.count()) if self.z2Box.itemText(i) != 'Все'])
        return all_values, self.selected_states['codprogBox']


    def remove_filter_button(self):

        self.start_combo()
        self.selected_states = {"codprogBox": 'Все', "regionBox": 'Все',
                                "oblnameBox": 'Все', "cityBox": 'Все', "z2Box": 'Все'}
        self.load_state()

    def db_loads(self, request):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.__db)
        db.open()
        query = QSqlQuery(request)
        column_values = []
        while query.next():
            column_value = query.value(0)
            column_values.append(column_value)
        db.close()
        return column_values
