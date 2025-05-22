from flask import Flask, render_template, request, redirect, make_response, url_for, session, flash
# from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MEGADIFICIL_ME_ESCONDE'

usuarios = {}
produtos = [
    {'id': 1, 'nome': 'Senhor dos Anéis', 'preco': 35},
    {'id': 2, 'nome': 'Harry Potter', 'preco': 35},
    {'id': 3, 'nome': 'Nárnia', 'preco': 20},
    {'id': 4, 'nome': 'Sherlock Holmes', 'preco': 25}
] 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=["GET","POST"])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get("usuario")
        senha = generate_password_hash(request.form.get("senha"))
        if nome in usuarios:
            return redirect(url_for('login'))
        else:
            usuarios[nome] = senha
            return redirect(url_for('login'))
    print(usuarios)
    return render_template('cadastro.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'POST':
        nome = request.form.get('usuario')
        senha = request.form.get('senha')
        if nome not in usuarios:         
            return redirect(url_for('cadastro'))

        if nome in usuarios and check_password_hash(usuarios[nome], senha):
            flash('Já cadastrado')
            session['nome'] = nome
            resp = make_response(redirect(url_for('produtos')))
            resp.set_cookie("nome", nome)
            return resp
    return render_template('login.html')

@app.route('/logout', methods=["POST"])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('index'))

@app.route('/produtos', methods=["GET", "POST"])
def produtos():
    if 'nome' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # getlist -- pega vários valores com o mesmo nome no formulário HTML
        selecionados = request.form.getlist('produto_id')
        selecionados_convertidos = []

        # Converte para uma lista de inteiros
        for id in selecionados:
            numero = int(id)
            selecionados_convertidos.append(numero)
            print(selecionados_convertidos)

        # Busca os produtos pelos IDs
        carrinho = session.get('carrinho', [])
        carrinho.extend(selecionados)

        session['carrinho'] = carrinho

        return redirect(url_for('carrinho'))

    return render_template('produtos.html', produtos=produtos)

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')


if __name__ == "__main__":
    app.run(debug=True)

