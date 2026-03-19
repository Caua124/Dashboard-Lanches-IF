from datetime import datetime
import sqlite3

#DATAS NO FORMATO DATETIME: (DD/MM/YYYY)
DATE_FORMAT = '%d/%m/%Y'

ITEM_TYPES = ('principal', 'complemento', 'fruta', 'bebida')
OCURRENCE_TYPES = ('merenda', 'almoço', 'janta')

WEEKDAY_CONVERSION_DICT = {
    'mon': 'seg', 
    'tue': 'ter', 
    'wed': 'qua',
    'thu': 'qui',
    'fri': 'sex',
    'sat': 'sab',
    'sun': 'dom'
}

"""COMO INSERIR DADOS MANUALMENTE? (faça pelo terminal, rode 'python' e dps from core import *)


insira todos os itens da refeição com o item_insert, um por vez, e se lembre de seus ids
insira a ocorrência, se for passar a data, use o formato certo, caso n vá, se certifique q a data do sistema está correta
insira os ids com a função ocurrence_item_insert(). Consulte usando o general query para ver se inseriu corretamente
se o insert falhou, tente descobrir o porquê e crie uma issue no github, caso n consiga resolver sozinho

Se lembre de dar connection.commit() e connection.close() após inserir os dados corretamente"""

#SEM COMMITS AUTOMÁTICOS NOS INSERTS (por enquanto)

connection = sqlite3.connect('database.db')
connection.execute('PRAGMA foreign_keys = ON')
cursor = connection.cursor()

def item_insert(name: str, i_type: str, c: sqlite3.Cursor = cursor) -> int | None:
    """Cria um novo item, recebe o tipo e o nome com args
    verifica por erros e se já há um item no banco
    verifique se já existe esse item no banco antes de inserir
    NÃO CRIA ASSOCIAÇÃO COM OCORRÊNCIAS!"""

    if not isinstance(i_type, str):
        raise TypeError('"i_type" deve ser uma string')
    elif i_type not in ITEM_TYPES:
        raise ValueError(f'"i_type" deve estar em {ITEM_TYPES}')
    
    if not isinstance(name, str):
        raise TypeError('"name" deve ser uma string')
    
    name = name.strip().lower()

    if not name:
        raise ValueError('"name" não pode ser vazio')
    #elif name.replace(' ', '') in [i.replace(' ', '') for i in c.execute('SELECT name FROM Item').fetchall()]:   NÃO FUNCIONA AINDA
    #    raise ValueError('Item já existe no banco de dados')

    c.execute(f'INSERT INTO Item (name, type) VALUES (?, ?)', (name, i_type))
    #connection.commit()

    return c.lastrowid

def ocurrence_insert(o_type: str, date: str = datetime.today().strftime(DATE_FORMAT), c: sqlite3.Cursor = cursor) -> int | None:
    """Cria uma nova ocorrência, recebe o tipo e a data com args
    Gera o dia da semana automaticamente, e verifica erros
    Se a data não for especificada, usa a data de hoje no sistema
    NÃO CRIA ASSOCIAÇÃO COM OS ITENS!"""

    if not isinstance(o_type, str):
        raise TypeError('"o_type" deve ser uma string')
    elif o_type not in OCURRENCE_TYPES:
        raise ValueError(f'"o_type" deve estar em {OCURRENCE_TYPES}')

    if not isinstance(date, str):
        raise TypeError('"date" deve ser uma string')
    
    date = date.strip()

    if not date:
        raise ValueError('"date" não pode ser vazio')
    elif (date, o_type) in c.execute('SELECT date, type FROM Ocurrence').fetchall():
        raise ValueError('Ocorrência já existe no banco de dados')

    try:
        dt_obj = datetime.strptime(date, DATE_FORMAT)
    except Exception as e:
        raise e('Formato de data inválido (DD/MM/AAAA)')
    
    weekday = WEEKDAY_CONVERSION_DICT.get(dt_obj.strftime('%a').lower())

    if not weekday:
        raise Exception('Erro inesperado. Não foi possível gerar um dia da semana')

    c.execute(f'INSERT INTO Ocurrence (date, weekday, type) VALUES (?, ?, ?)', (date, weekday, o_type))
    #connection.commit()
    
    return c.lastrowid

def ocurrence_item_insert(oc_id: int, item_ids: list[int], c: sqlite3.Cursor = cursor) -> None:
    for item_id in item_ids:
        c.execute(f'INSERT INTO OcurrenceItem (ocurrence_id, item_id) VALUES (?, ?)', (oc_id, item_id))

    #connection.commit()

#3 consultas básicas
def item_query(c: sqlite3.Cursor = cursor) -> list[tuple]:
    values = c.execute('SELECT * FROM Item').fetchall()

    return values

def ocurrence_query(c: sqlite3.Cursor = cursor) -> list[tuple]:
    values = c.execute('SELECT * FROM Ocurrence').fetchall()

    return values

def ocurrence_item_query(c: sqlite3.Cursor = cursor) -> list[tuple]:
    values = c.execute('SELECT * FROM OcurrenceItem').fetchall()

    return values

#Dar uma corrigida, fiz antes de descobrir como ativar as FK com o PRAGMA ( mas funciona normal, só tá mais confuso doq deveria )
def general_query(c: sqlite3.Cursor = cursor) -> list[tuple]:
    values = c.execute('SELECT date, o.type, name, i.type FROM Ocurrence o JOIN OcurrenceItem oi ON o.id = oi.ocurrence_id JOIN Item i ON i.id = oi.item_id').fetchall()

    return values

if __name__ == '__main__':
    print(item_query(), '- Item\n')
    print(ocurrence_query(), '- Ocurrence\n')
    print(ocurrence_item_query(), '- OcurrenceItem\n')
    print(general_query())
    connection.close()