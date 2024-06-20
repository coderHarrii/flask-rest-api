# Flask

É um microweb framework em python por que não precisa de bibliotecas e não possui componentes extra incluídos, além de permitir a adição de bibliotecas e ser fácil de construir, geralmente utilizado para construir resful APIs.

# Commands

### environment
pip install venv

### create environment
python -m venv env

### activate environment
source env/bin/activate

### install flask and its dependencies
pip install flask

### show packages
pip freeze

### install packages
pip freeze -r requirements.txt

### create package list
pip freeze > requirements.txt

# WSGI
Web service gateway interface é uma interface que faz a ponte de interação entre servdores web e aplicativos python. Ele recebe requisições e as converte em chamadas de função. Um app flask é na verdade um aplicativo WSGI.

# Run WSGI (or Flask) by Environment Variable
Precisamos que o comando "Flask run" encontre o aplicativo Flask instanciado na variável de ambiente FLASK_APP, por isso, damos export em app.py como FLASK_APP
- export FLASK_APP=app.py
- Flask run

# Run WSGI (or Flask) progammatically
Basicamente, quando o módulo é executado diretamente, o nome dele é "__main__" e daí app.run é chamado, mas se o módulo for chamado por outro módulo, "__name__" é definido como o nome desse módulo, ou seja, o nome do arquivo sem a extensão ".py".

Podemos executar o servidor através da verificação main da seguinte forma:

    if __name__ == '__main__':
        app.run()

E executar o app.py:

    python app.py

# Debbuging

## Reloader
Observa todas as mudanças em arquivos e reinicia o servidor quando alguma mudança é detectada. É ótimo no desenvolvimento.

    flask run --reload

Por padrão o reloader é ativo quando executamos debugger.

## Debugger
É uma ferramenta que observa exceptions pelo navegador. A janela permite interagir com o código como uma pilha em vez de expor o erro HTTP na tela.

Se estiver executando flask através de variável de ambiente, então ative através do comando:

    export FLASK_DEBUG=1

Se estiver executando fask programaticamente, ative com:
    if __name__ == '__main__':
        app.run(debug=True)

# Help
    flask --help
    flask run --help

# Host
Flask por padrão roda no ip localhost, porém podemos alterar isso no deploy ao executar o seguinte comando:

    flask run --host <DEPLOY-MACHINE-IP>

# Request-Response Cycle

## Big Picture
CLiente cria requisição e flask cria objetos para a view resolver, essa requisição é encapsulada como uma requisição http que é recebida como parametro na view. O servidor espera que a view retorne uma resposta para aquela requisição que então é retornada ao cliente.

## Aplication & Request Context
Vamos supor que a view precise acessar mais de um objeto, ou seja, além do objeto request. Precisamos passar mais de um objeto como argumento. Para isso, Flask usa o que chamamos de Context para fazer variáveis se tornarem globais temporariamente.

*Obs: Na realidade as req não podem ser variáveis globais, pois num app multithread cada thread precisa de um objeto HTTP para sua requisição específica.

Context: Consegue realizar a observação anterior para outros objetos (não http) serem globais dentro de uma thread, sem interferir no espaço de memória de outra

#### Application context
- current_app: É uma instância da aplicação Flask ativa.
- g: É um objeto global temporário que a aplicação pode usar durante o tempo de vida de uma única requisição, ou seja, em cada thread sem que haja memória compartilhada.

Quando app_context.push() é chamado, current_app e g ficam ativos na thread atual.

#### Request context
- request: é o request atual que é criado a partir do usuário
- session: é um dicionario que o app pode usar para armazenar valores que são lembrados entre requisições, com dados do usuário autenticado. Cada posição do dicionario corresponde a um par thread-data

Quando request_context.push() é chamado, request e session ficam ativos na thread da requisição daquele usuário.

## Request dispatching
Quando o Flask server recebe uma requisição, ele precisa saber qual view chamar para processar aquela requisição. Para isso, o WSGI olha qual é a rota da view daquela requisição no "applications url map". 

## Request Object Methods
- get_data: retorna os dados bufferizados
- get_json: retorna os dados bufferizados no corpo do objeto
- is_secure: retorna true se a req vem de uma conexão https

## Request Object Variables
- endpoint: É um ponto final para o objeto naquela direção ser processado. 
- method: Get ou post
- host: é o nome do servidor
- url: endereço da requisição
- environ: é um dicionario com várias variáveis de ambiente CGI (Common Gateway Interface) da requisicao

## Request Hooks
São funções que podem ser programadas para serem chamadas em momentos específicos, como antes ou depois de uma requisição ser processada. Temos quatro:
- before_request
- before_first_request
- after_request
- teardown_request

Aqui nós usamos application context, através do objeto g 

## Response Values
A resposta pode vir com até três valores em um unico objeto:
- Resposta http
- Código de status
- headers: tem infos adicionais sobre a resposta

## Response Methods
A resposta vem com os seguintes métodos:
- set_cookie: Adiciona cookie na resposta
- delete_cookie: Remove cookie
- set_data: Seta o corpo com byte values
- get_data: Recebe esses byte values

## Response Variables
Temos as seguintes:
- status_code
- headers
- contet_length
- content_type

## Response Redirect
Não retorna página ou string, mas sim uma url navegavel

# RESTful API
A representational state transform é um meio de comunicação entre duas máquinas via HTTP. Uma comunicação REST deve ser:
- Arquitetura Cliente-servidor
- Stateless: A requisição do usuário deve conter tudo que o servidor precisa para processar a requisição
- Cachable: Uma resposta precisa ser classificada como cachable ou não
- Layered: O cliente não pode saber se está se comunicando com um proxy, um servidor real ou algum intermediário

## Important Terminologies
- Endpoint/Resource: URL + DOMAIN + PORT + PATH + QUERY 
- HTTP Methods (CRUD): GET, POST, PUT, DELETE
- HTTP Headers: Authentication Token, Cookies etc

## JSON
Javascript Object Notation é uma linguagem baseada em js que intercambia dados

# Database
Podemos usar uma implementação de api rest que armazena dados em uma lista encadeada ou em um banco de dados relacional, como o sqlite e o mysql.

## SQLite
É um dos databases mais utilizados no mundo e é:
- Pequeno e rápido
- Escrito em C
- Usado em grande parte de dispositivos mobile e desktop

# Postman
Podemos realizar teste via postman ao usar a seguinte configuração de request:
- Criar uma request POST, GET, PUT ou DELETE e para cada uma delas criar uma estrutura raw formatada em JSON com as seguinte variáveis:

{
    "author": "Harrison",
    "language": "Brazilian",
    "title": "This is a simple rest api doc"
}