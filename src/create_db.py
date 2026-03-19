import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#Esse arquivo tem apenas a finalidade de salvar esse script
if __name__ == '__main__':
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ocurrence(
            ocurrence_id INTEGER PRIMARY KEY,
            date TEXT,
            ocurrence_type TEXT,
            weekday TEXT);""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item(
            item_id INTEGER PRIMARY KEY,
            name TEXT,
            item_type TEXT);""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OcurrenceItem(
            ocurrence_id INTEGER,
            item_id INTEGER,
                   
            PRIMARY KEY(ocurrence_id, item_id),
                   
            FOREIGN KEY (ocurrence_id) REFERENCES Ocurrence(ocurrence_id),
            FOREIGN KEY (item_id) REFERENCES item(item_id));""")
