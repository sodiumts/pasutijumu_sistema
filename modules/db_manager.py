import sqlite3

class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table("USERS", "User_ID INTEGER PRIMARY KEY,Name_Surname,Person_code TEXT,Username TEXT,Password TEXT,ACCESS_LEVEL INTEGER")

        # self.create_table("ORDER","Order_ID INTEGER PRIMARY KEY,Order_Nr,Organizacija,Datums,Apmaksats,Order_Received,Apm_Datums,User_ID")
        self.create_table("ORDER_DETAIL","Order_Detail_ID INTEGER PRIMARY KEY,Order_ID,Order_Address,Order_Detail,Payment_Status")
        self.create_table("ORDERS","Order_ID INTEGER PRIMARY KEY,Organizacija,Datums,Apmaksats,Order_Received,Apm_Datums,User_ID")
    def create_table(self, table_name, fields):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}({fields})")
        self.conn.commit()

    def insert(self, table_name, fields, values):
        self.cursor.execute(f"INSERT INTO {table_name}({fields}) VALUES({values})")
        self.conn.commit()

    def select(self, table_name, fields, condition):
        self.cursor.execute(f"SELECT {fields} FROM {table_name} WHERE {condition}")
        return self.cursor.fetchall()

    def update(self, table_name, fields, condition):
        self.cursor.execute(f"UPDATE {table_name} SET {fields} WHERE {condition}")
        self.conn.commit()

    def delete(self, table_name, condition):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.conn.commit()

    def close(self):
        self.conn.close()
