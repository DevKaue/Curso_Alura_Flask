import os

from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import recupera_imagem
import time

@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novoJogo')
def novoJogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novoJogo')))
    return render_template('novoJogo.html',titulo='Novo Jogo')

@app.route('/criarJogo', methods=['POST',])
def criarJogo():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))

    novo_Jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_Jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_Jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html',titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='Login', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' Usuario logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha incorreta')
            return redirect(url_for('login'))
    else:
        flash('Usuario não autorizado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

