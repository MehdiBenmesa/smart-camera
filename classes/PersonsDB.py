import sqlite3 as lite
TABLE_LINK = 'persons.db'


class PersonsDB():
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        try:
            self.conn = lite.connect(TABLE_LINK)
            self.cursor = self.conn.cursor()

        except lite.Error as e:
            print("Error connecting to database!")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def query_person(self, id):
        query = "SELECT * FROM Persons WHERE id="+str(id)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows[0]

    def insert_person(self, name, lastname, birthday, email, company):
        query = "INSERT INTO Persons (name, lastname, birthday, email, company) VALUES ( :name, :lastname, :birthday, :email, :company)"
        self.cursor.execute(query, {'name': name, 'lastname': lastname, 'birthday': birthday, 'email': email, 'company': company})
        return self.cursor.lastrowid

