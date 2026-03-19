#Esse arquivo tem apenas a finalidade de salvar esse script

if __name__ == '__main__':
    import sqlite3

    connection = sqlite3.connect('database.db')
    connection.execute('PRAGMA foreign_keys = ON')
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ocurrence(
            id INTEGER NOT NULL PRIMARY KEY UNIQUE,
            date TEXT NOT NULL,
            weekday TEXT NOT NULL,
            type TEXT NOT NULL);""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Item(
            id INTEGER NOT NULL PRIMARY KEY UNIQUE,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL);""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS OcurrenceItem(
            ocurrence_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
                   
            PRIMARY KEY(ocurrence_id, item_id),
                   
            FOREIGN KEY (ocurrence_id) REFERENCES Ocurrence(id) ON DELETE CASCADE,
            FOREIGN KEY (item_id) REFERENCES Item(id) ON DELETE CASCADE);""")
    
    connection.commit()
    connection.close()