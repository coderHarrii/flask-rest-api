from flask import Flask
from flask import current_app
from flask import g
from flask import session

# o webserver passa todos os requests para esse objeto wsgi (web server gateway interface)
# o argumento aqui é o nome do pacote
# aqui estamos instanciando um aplicativo flask, que é na verdade um aplicativo WSGI
app = Flask(__name__)

# ----------------- application context -----------------
# @app.route('/')
# def some_function()):
#     # current_app é uma referencia a instancia Flask que esta em execucao agora
#     print(current_app.name)

# # defino aqui um valor temporário que será usado por algumas threads apenas localmente em sua memória virtualizada
# @app.before_request
# def before_request():
#     g.some_data = "temporarie value"


# Aqui estou ativando o application context com current_app e g
with app.app_context():
    print(current_app.name)
    g.some_data = "temporarie value"

# ----------------- request context -----------------

# para lidar com as requisicoes vamos criar as chamadas rotas para views
# rotas sao caminhos para levar requisições até as funções que tratam essas requisicoes

# é o objeto que representa uma requisição http, utilizado para acessar dados da requisição
@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return f"Seu navegador é {user_agent}"

@app.route('/set/')
def set_session():
    session['user_id'] = 42
    return "defined session"

@app.route('/get/')
def get_session():
    return session['user_id']

# ---------------------------------------------------

@app.route('/<name>')
def print_name(name):
    return 'Hi, {}'.format(name)

# quando o módulo é executado diretamente, o nome dele é __main__ e daí app.run é chamado
# mas se o módulo for chamado por outro módulo, __name__ é definido como o nome desse módulo, ou seja, o nome do arquivo
# sem a extensão .py
if __name__ == '__main__':
        app.run(debug=True)