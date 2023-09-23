from info_form import Info_Form


class Ntp_Info(Info_Form):

    def __init__(self):
        self.__db = "SUBDlab.db"
        self.__tb_name = "ntp_prog"
        # возможно тут стоит поменять порядок столбцов и укоротить названия
        self.__request = f"""SELECT codprog AS "код НТП",
                                    prog AS "название НТП",
                                    nproj AS "количество проектов",
                                    pfin AS "плановое финансирование текущего года",
                                    pfin1 AS "к. 1 плановое финансирование",
                                    pfin2 AS "к. 2 плановое финансирование",
                                    pfin3 AS "к. 3 плановое финансирование",
                                    pfin4 AS "к. 4 плановое финансирование",
                                    ffin AS "фактическое финансирование текущего года",
                                    ffin1 AS "к. 1 фактическое финансирование текущего года",
                                    ffin2 AS "к. 2 фактическое финансирование текущего года",
                                    ffin3 AS "к. 3 фактическое финансирование текущего года",
                                    ffin4 AS "к. 4 фактическое финансирование текущего года"       
                            FROM {self.__tb_name}"""
        super().__init__(self.__db, self.__tb_name, self.__request)