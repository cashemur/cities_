import sqlite3 as sql

con = sql.connect('test.db')


class GameClass:

    def __init__(self, usersValue):
        self.usersValue = usersValue
        self.exist_condition = self.is_exist()

    def normalize(self):
        self.usersValue = self.usersValue[0].upper() + self.usersValue[1:].lower()
        return self.usersValue

    def is_exist(self):
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT cities from '_cities' WHERE cities = '{self.usersValue}' AND isUsed = 'false';")
            self.rows = cur.fetchone()
            if self.rows == None:
                return False
            else:
                return True

    def normalize_user_answer(self):
        if self.exist_condition:
            with con:
                cur = con.cursor()
                i = 1
                cur.execute(f"UPDATE _cities SET isUsed = 'true' WHERE cities LIKE '{self.usersValue}';")
                while self.usersValue[-i] == "ь" or self.usersValue[-i] == "ъ" or self.usersValue[-i] == "й" or \
                        self.usersValue[-i] == "ы" or self.usersValue[-i] == "э" or self.usersValue[-i] == " " or self.usersValue[-i] == "-":
                    self.usersValue = self.usersValue[:len(self.usersValue) - i]
            return self.usersValue

    def get_computer_answer(self):
        if self.exist_condition:
            i = 1
            with con:
                cur = con.cursor()
                cur.execute(
                    f"SELECT field5 from '_cities' WHERE cities LIKE '{self.usersValue[-i].upper()}%' AND isUsed = 'false';")
                self.answer = cur.fetchone()
                cur.execute(f"UPDATE _cities SET isUsed = 'true' WHERE cities LIKE '{self.answer[0]}%';")
                while self.answer == None:
                    cur.execute(
                        f"SELECT field5 from '_cities' WHERE cities LIKE '{self.usersValue[-i].upper()}%' AND isUsed = 'false';")
                    self.answer = cur.fetchone()
                    cur.execute(f"UPDATE _cities SET isUsed = 'true' WHERE cities LIKE '{self.answer[0]}%';")

                return self.answer[0]
        else:
            return "Used"


