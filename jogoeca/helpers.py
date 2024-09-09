import os
from wsgiref.validate import validator

import validators
from wtforms.fields.simple import StringField, SubmitField

from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import  StringField, validators

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do jogo', [validators.DataRequired(), validators.Length(min=1,max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1,max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1,max=20)])
    salvar = SubmitField('Salvar')

# função para recuperar imagem do jogo
def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'

#Função para deletar arquivo duplicado
def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        caminho_arquivo = os.path.join(app.config['UPLOAD_PATH'], arquivo)
        if os.path.exists(caminho_arquivo):  # Verifica se o arquivo existe
            try:
                os.remove(caminho_arquivo)
            except FileNotFoundError:
                print(f"Arquivo {arquivo} não encontrado.")
            except Exception as e:
                print(f"Erro ao remover o arquivo: {e}")