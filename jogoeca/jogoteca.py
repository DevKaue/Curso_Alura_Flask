from flask import Flask, render_template, request, redirect, session, flash

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console


jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1,jogo2,jogo3]

app = Flask(__name__)
app.secret_key = 'teste_flask'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novoJogo')
def novo():
    return render_template('novoJogo.html',titulo='Novo Jogo')

@app.route('/criarJogo', methods=['POST',])
def criarJogo():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)

    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html', titulo='Login')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if 'alohomora' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(session['usuario_logado'] + 'Usuario logado com sucesso!')
        return redirect('/')
    else:
        flash('Usuario não autorizado')
        return redirect('/login')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/login')

app.run(debug=True)
