import sqlite3

# aqui nós estabelecemos conexão com o arquivo (que abstrai) do banco de dados
conn = sqlite3.connect('books.sqlite')

# o objeto cursor é utilizado para executar declarações SQL,
# é como uma interface entre o programa e o banco de dados
cursor = conn.cursor()
sql_query = """ CREATE TABLE book (
    id integer PRIMARY KEY,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
    )"""

cursor.execute(sql_query)