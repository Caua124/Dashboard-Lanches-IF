import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#Esse arquivo tem apenas a finalidade de salvar
if __name__ == '__main__':
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ocurrence(
            id INTEGER PRIMARY KEY,
            date TEXT,
            type TEXT);""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT);""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OcurrenceItem(
            ocurrence_id INTEGER,
            item_id INTEGER,
                   
            PRIMARY KEY(ocurrence_id, item_id),
                   
            FOREIGN KEY (ocurrence_id) REFERENCES Ocurrence(id),
            FOREIGN KEY (item_id) REFERENCES item(id));""")