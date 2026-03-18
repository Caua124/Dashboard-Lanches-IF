from datetime import datetime
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

#DATAS NO FORMATO DATETIME: (DD/MM/YYYY)
#TIPOS DE ITEM: principal, complemento, fruta, bebida
#TIPOS DE OCORRÊNCIA: merenda, almoço, janta
#DIAS DA SEMANA: seg, ter, qua, qui, sex

def item_insert(name: str, type: str, c: sqlite3.Cursor = cursor) -> int | None:
    #Adicionar verificação prévia, para não repetir items já existentes
    #Verificar também o tipo, vou deixar uns pré-definidos (talvez não seja necessário)

    c.execute(f'INSERT INTO Item (name, item_type) VALUES (?, ?)', (name, type))
    return c.lastrowid

def ocurrence_insert(date: str, type: str, weekday: str, c: sqlite3.Cursor = cursor) -> int | None:
    #Mesmas observações prévias
    
    if not datetime.strptime(date, '%d/%m/%Y') or date.strip() == '':
        raise ValueError
        #necessita de testes

    c.execute(f'INSERT INTO Ocurrence (date, ocurrence_type, weekday) VALUES (?, ?, ?)', (date, type, weekday))
    return c.lastrowid

def ocurrence_item_insert(oc_id: int, item_ids: list[int], c: sqlite3.Cursor = cursor) -> None:
    for item_id in item_ids:
        c.execute(f'INSERT INTO OcurrenceItem (ocurrence_id, item_id) VALUES (?, ?)', (oc_id, item_id))

def terminal_insert():
    #TEMPORÁRIO
    #se acontecer algum problema e inserir uma ocorrência mas falhar em inserir todos os itens dela, apague ela e tente dnv
    #essa função é bem simples mesmo, seu propósito é só permitir salvar dados logo, enquanto não faço algo melhor

    oc_id = ocurrence_insert(input('data: '), input('tipo: '), input('dia da semana: '))

    item_ids = []
    while True:
        inp = input('insira o id do item, 0 para sair: ')
        if inp == '0':
            break

        item_ids.append(int(inp))

    ocurrence_item_insert(oc_id, item_ids)

def general_query() -> list:
    #necessita de melhorias

    return cursor.execute('SELECT date, GROUP_CONCAT(name) FROM Ocurrence o JOIN OcurrenceItem oi ON o.id = oi.ocurrence_id JOIN Item i ON i.id = oi.item_id').fetchall()

if __name__ == '__main__':
    print(cursor.execute('SELECT * FROM Item').fetchall())
    print(cursor.execute('SELECT * FROM Ocurrence').fetchall())
    print(cursor.execute('SELECT * FROM OcurrenceItem').fetchall())
    print(general_query())
    connection.close()