from base_form import Base_Form


class Ntp_Info(Base_Form):

    def __init__(self):
        self.__db = "SUBDlab.db"
        self.__tb_name = "ntp_prog"
        self.__request = f"""SELECT codprog AS "код НТП",
                                    prog AS "название НТП",
                                    nproj AS "количество проектов",
                                    pfin AS "план. фин. на год",
                                    pfin1 AS "план. фин. кв. 1",
                                    pfin2 AS "план. фин. кв. 2",
                                    pfin3 AS "план. фин. кв. 3",
                                    pfin4 AS "план. фин. кв. 4",
                                    ffin AS "факт. фин. тек. года",
                                    ffin1 AS "факт. фин. кв. 1",
                                    ffin2 AS "факт. фин. кв. 2",
                                    ffin3 AS "факт. фин. кв. 3",
                                    ffin4 AS "факт. фин. кв. 4"            
                            FROM {self.__tb_name}
                            ORDER BY codprog, prog"""
        super().__init__(self.__db, self.__tb_name, self.__request)