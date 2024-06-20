# request - permite usar métodos do objeto http
# jsonify - codifica dicionários python em json 
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# estabelecemos conexão com o db primeiro
def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('books.sqlite')
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        # damos READ no db ao criar uma lista de dicionários para todos
        # usamos uma list comprehension para iterar sobre cada tupla retornada por fetchall
        cursor = conn.execute('SELECT * FROM book')
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()
        ]    
        
        if books is not None:
            return jsonify(books), 200
        else:
            'Not Found', 404
    
    if request.method == 'POST':
        # recebo os dados JSON do corpo da requisicao
        data = request.get_json()
        
        new_author = data['author']
        new_lang = data['language']
        new_title = data['title']
        
        # criamos nossa query, em que os pontos de interrogação
        # são inputs para passarmos valores dinamicamente
        sql_query = """ INSERT INTO book (author, language, title)
                        VALUES (?, ?, ?)"""
        
        # nós executamos o comando no db
        cur = cursor.execute(sql_query, (new_author, new_lang, new_title))
        
        # persistimos as alterações feitas, ou seja, salvamos o insert
        conn.commit()

        return "Book with the id: {} created successfully".format(cursor.lastrowid), 201
    
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    
    if request.method == 'GET':
        # novamente, o ponto de interrogação é um placeholder
        cursor.execute('SELECT * FROM book WHERE id=?', (id,))
        rows = cursor.fetchall()
        
        for r in rows:
            book = r 
            
        if book is not None:
            return jsonify(book), 200
        else:
            'Something wrong', 404
    
    if request.method == 'PUT':
        data = request.get_json()

        sql_query = """UPDATE book 
                SET title=?,
                    author=?,
                    language=?
                WHERE id=?"""
                                      
        new_author = data['author']
        new_lang = data['language']
        new_title = data['title']
                
        updated_book = {
            'id': id,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }
        
        conn.execute(sql_query, (new_author, new_lang, new_title, id))
        conn.commit()
                
        return jsonify(updated_book), 200

    if request.method == 'DELETE':
        sql_query = """DELETE FROM book WHERE id=?"""
        
        conn.execute(sql_query, (id,))
        return 'The book with id: {} has been deleted'.format(id), 200

# quando o módulo é executado diretamente, o nome dele é __main__ e daí app.run é chamado
# mas se o módulo for chamado por outro módulo, __name__ é definido como o nome desse módulo, ou seja, o nome do arquivo
# sem a extensão .py
if __name__ == '__main__':
        app.run(debug=True)