from flask import Flask, \
    render_template, \
    request, redirect, \
    session, \
    flash, \
    url_for, \
    send_from_directory

from models import Jogo, Usuario
from dao import JogoDao, UsuarioDao
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'alura'
app.config['UPLOAD_PATH'] = f'{os.path.dirname(os.path.abspath(__file__))}/uploads'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "root"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306
db = MySQL(app)

jogoDao = JogoDao(db)
userDao = UsuarioDao(db)
@app.route('/')
def index():
    lista = jogoDao.listar()
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo = jogoDao.salvar(jogo)
    uploadPath = app.config['UPLOAD_PATH']
    arquivo = request.files['arquivo']
    arquivo.save(f"{uploadPath}/capa_{jogo.id}.png")
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogoDao.busca_por_id(id)
    capa_jogo = f'capa_{id}.png'
    return render_template('editar.html', titulo='Editar Jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    id = request.form['id']
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id)
    jogoDao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    jogoDao.deletar(id)
    flash('O jogo foi deletado com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = userDao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    flash('Não logado, tente novamente!')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

app.run(debug=True)
