from info_form import Info_Form


class Vuz_Info(Info_Form):

    def __init__(self):
        self.__db = "SUBDlab.db"
        self.__tb_name = "vuz"

        # возможно тут стоит поменять порядок столбцов и укоротить названия
        self.__request = f"""SELECT codvuz AS "код вуза",
                                    z1 AS "наименование вуза",
                                    z1full AS "полное юридическое наименование вуза",
                                    z2 AS "сокращенное наименование",
                                    region AS "федеральный окру",
                                    city AS "город",
                                    status AS "статус",
                                    obl AS "номер субъекта федерации",
                                    oblname AS "субъект федерации",
                                    gr_ved AS "принадлежность к ведущим вуза",
                                    prof AS "профиль вуза"      
                            FROM {self.__tb_name}"""
        super().__init__(self.__db, self.__tb_name, self.__request)