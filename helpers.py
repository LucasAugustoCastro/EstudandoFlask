import os
from jogoteca import app
def recuperaImagem(id):
    for nomeArquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nomeArquivo:
            return nomeArquivo

def deletar_arquivo(id):
    arquivo = recuperaImagem(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))