# request - permite usar métodos do objeto http
# jsonify - codifica dicionários python em json 
from flask import Flask, request, jsonify

app = Flask(__name__)

# aqui nós temos um banco de dados como uma lista de dicionários
books_list = []

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
            if len(books_list) > 0:
                return jsonify(books_list)
            else:
                'Nothing Found', 404
    
    if request.method == 'POST':
        # recebo os dados JSON do corpo da requisicao
        data = request.get_json()
        
        if len(books_list) == 0:
            book_id = 0
        else:
            # aqui acesso o ultimo item da lista, obtenho o id dele e somo 1
            book_id = books_list[-1]['id']+1
            
        new_author = data['author']
        new_lang = data['language']
        new_title = data['title']
        
        new_obj = {
            'id': book_id,
            'author': new_author,
            'language': new_lang,
            'title': new_title
        }
        
        books_list.append(new_obj)
        return jsonify(books_list), 201
    
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    if request.method == 'GET':
        for book in books_list:
            if book['id'] == id:
                return jsonify(book)
    
    if request.method == 'PUT':
        data = request.get_json()
        for book in books_list:
            if book['id'] == id:
                book['author'] = data['author']
                book['language'] = data['language']
                book['title'] = data['title']
                
                updated_book = {
                    'id': id,
                    'author': book['author'],
                    'language': book['language'],
                    'title': book['title']
                }
                
                return jsonify(updated_book)

    if request.method == 'DELETE':
        for index, book in enumerate(books_list):
            if book['id'] == id:
                books_list.pop(index)
                return jsonify(books_list)

# quando o módulo é executado diretamente, o nome dele é __main__ e daí app.run é chamado
# mas se o módulo for chamado por outro módulo, __name__ é definido como o nome desse módulo, ou seja, o nome do arquivo
# sem a extensão .py
if __name__ == '__main__':
        app.run(debug=True)