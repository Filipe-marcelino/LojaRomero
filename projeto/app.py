from flask import Flask, render_template, request, redirect, make_response, url_for, session
# from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MEGADIFICIL_ME_ESCONDE'
usuarios = {}
produtos = [
    {'id': 1, 'nome': 'Senhor dos Anéis', 'preco': 20},
    {'id': 2, 'nome': 'Harry Potter', 'preco': 25},
    {'id': 3, 'nome': 'As Crônicas de Nárnia', 'preco': 30},
    {'id': 4, 'nome': 'Anne de Green Gables', 'preco': 25},
    {'id': 3, 'nome': 'Sherlock Holmes', 'preco': 35},
] 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    if request.method == 'POST':
        nome = request.form.get("usuario")
        senha = generate_password_hash(request.form.get("senha"))

        if nome in usuarios:
            return redirect(url_for('cadastro'))
        
        usuarios[nome] = senha
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login')
def login():
    if request.method == 'POST':
        nome = request.form.get('usuario')
        senha = request.form.get('senha')
        if nome in usuarios and check_password_hash(usuarios[nome], senha):
            session['nome'] = nome
            resp = make_response(redirect(url_for('produtos')))
            resp.set_cookie('usuario','usuario',max_age=60*60)

        return redirect(url_for('cadastro'))
    return render_template('login.html')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')




# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         nome = request.form.get('nome')
#         senha = request.form.get('senha')

#         senha_criptografada = generate_password_hash(senha)

#         if nome not in usuarios:         
#             usuarios[nome] = senha_criptografada
#             flash("Cadastro realizado com sucesso!")
#             return redirect(url_for('login'))
#         if nome in usuarios and check_password_hash(usuarios[nome], senha):
#             flash("Você já está cadastrado")
#             return redirect(url_for('login'))

#     return render_template('register.html')

# @app.route('/login', methods=['POST', 'GET'])
# def login():

#     if request.method == 'POST':
#         nome = request.form.get('nome')
#         senha = request.form.get('senha')
#         senha_criptografada = generate_password_hash(senha)

#         if nome not in usuarios:
#             return redirect(url_for('register'))
#         if nome in usuarios and check_password_hash(usuarios[nome], senha):
#             # logar o usuário
#             session['user'] = nome
#             session['senha_criptografada'] = senha_criptografada
#             return redirect(url_for('dash'))
#         else:
#             return redirect(url_for('register'))

#     return render_template('login.html')