import os.path

from django.conf import settings
from pathlib import Path
from PIL import Image
from django.contrib.auth.models import User
from _datetime import datetime
import hashlib
from galeria.models import Tag, Photo, Collection

def salva_imagens(dados):
    try:
        # BUSCA A COLLECTION, SE NAO EXISTIR CRIA UMA NOVA
        try:
            collection = Collection.objects.get(author=dados['author'], title=dados['collection'])
        except:
            try:
                collection = Collection.objects.create(author=dados['author'], title=dados['collection'])
            except:
                return {'erro': True, 'mensagem': "Houve um erro ao criar a Coleção"}

        # BUSCA A TAG, SE NAO EXISTIR CRIA UMA NOVA
        if dados['tags']:
            try:
                tag = Tag.objects.get(name=dados['tags'])
            except:
                try:
                    tag = Tag.objects.create(name=dados['tags'])
                except:
                    return {'erro': True, 'mensagem': "Houve um erro ao criar a Tag"}

        # SALVA AS IMAGENS
        imagens = dados['imagens']
        project_path = settings.BASE_DIR
        project_path = project_path.as_posix()
        path = '/galeria/arquivos/imagens/'
        for imagem in imagens:
            extensao = '.jpg' if imagem.name.lower().endswith(('.jpg', '.jpeg')) else '.png'
            data_hora = datetime.now()
            hash = hashlib.md5()
            arquivo = str(data_hora) + '_' + str(dados['author'].pk)
            hash.update(arquivo.encode('utf-8'))
            nome_arquivo = hash.hexdigest() + extensao
            caminho_completo = Path(project_path + path + nome_arquivo)
            img = Image.open(imagem.file)
            img = img.save(caminho_completo)

            try:
                photo = Photo.objects.create(
                    author=dados['author'],
                    collection=collection,
                    archive=nome_arquivo,
                    isFavorite=dados['favorite'],
                    created_date=dados['creation_date']
                )

                # Associar as tags após a criação da foto
                if dados['tags']:
                    photo.tags.add(tag)
            except Exception as err:
                print(err)
                pass
        return True
    except Exception as err:
        print(err)
        return False, {'erro': 'True', 'mensagem': 'ocorreu um erro: ' + str(err)}


def cria_usuario(dados):
    pode_criar = False
    try:
        busca = User.objects.get(username=dados['username'])
        return {'erro': True, 'mensagem': 'O username ' + dados['username'] + ' não está disponível!', 'cadastrar': True}
    except:
        try:
            busca = User.objects.get(email=dados['email'])
            return {'erro': True, 'mensagem': 'Email já cadastrado!', 'cadastrar': True}
        except:
            pode_criar = True

    try:
        if pode_criar:
            user = User.objects.create_user(dados['username'], dados['email'], dados['password'],
                                            first_name=dados['first_name'], last_name=dados['last_name'], is_active=True,
                                            is_staff=False, is_superuser=False, date_joined=datetime.now())
            return {'sucesso': True}
    except:
        return {'erro': True, 'mensagem': 'Ocorreu um erro inesperado. Parece que estamos tendo dificuldades para crair seu usuário', 'cadastrar': True}


def busca_imagens(user, colecao=None):

    if colecao:
        collection = Collection.objects.get(author=user, title=colecao)
        imagens = Photo.objects.filter(author=user, collection=collection)
    else:
        if user.is_authenticated:
            imagens = Photo.objects.filter(author=user)
        else:
            imagens = Photo.objects.filter()

    retorno = []

    for imagem in imagens:
        retorno.append(imagem.archive)


    return retorno


def busca_colecoes(user):
    opcoes = []
    colecoes = Collection.objects.filter(author=user)

    opcoes.append(('0', 'Não selecionado'))

    for colecao in colecoes:
        opcao = (str(colecao.title), str(colecao.title))
        opcoes.append(opcao)

    return opcoes


def colecoes(user):

    colecoes = Collection.objects.filter(author=user)
    dic = {}

    for colecao in colecoes:
        dic[colecao.title] = []
        photos = Photo.objects.filter(collection=colecao, author=user)
        for photo in photos:
            dic[colecao.title].append(photo.archive)

    return dic


def favoritos(user):
    dic = []

    favorito = Photo.objects.filter(author=user, isFavorite=True)

    for fav in favorito:
        dic.append(fav.archive)

    return dic