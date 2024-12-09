from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404
from django.shortcuts import render, HttpResponse, redirect
from galeria.forms import FormAdiciona, FormLogin, FormCadastro
from galeria.funcoes import salva_imagens, cria_usuario, busca_imagens, colecoes, favoritos
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from _datetime import datetime
import json

# Create your views here.

@login_required
def Home(request):

  photos = busca_imagens(request.user)

  dic = {'photos': photos}

  return render(request, 'home.html', dic)

@login_required
def Adiciona(request):
  dic = {}
  form = FormAdiciona(user=request.user)

  if request.method == 'POST':
    form = FormAdiciona(request.POST, user=request.user)
    if form.is_valid():


      dados = {
        'tags': form.cleaned_data['tags'],
        'favorite': form.cleaned_data['favorite'],
        'collection': form.cleaned_data['new_collection'] if form.cleaned_data['new_collection'].strip() else form.cleaned_data['pick_collection'],
        'creation_date': datetime.now(),
        'author': request.user,
        'imagens': request.FILES.getlist('imagens')
      }

      resultado = salva_imagens(dados)
      if resultado:
        dic['retorno'] = {'sucesso': True, 'mensagem': "Imagens cadastradas com sucesso!"}
        return render(request, 'adiciona_imagens.html', dic)
      else:
        pass

  dic['form'] = form

  return render(request, 'adiciona_imagens.html', dic)


def recebe_login(request):
  dic = {}
  form = FormLogin()

  if request.method == 'POST':
    form = FormLogin(request.POST)
    if form.is_valid():
      authenticate_user = authenticate(
        username=form.cleaned_data.get('username', ''),
        password=form.cleaned_data.get('password', ''),
      )
      if authenticate_user is not None:
        login(request, authenticate_user)
        dic['retorno'] = {'sucesso':True, 'mensagem': "Login Efetuado com sucesso"}
        return redirect('/')
      else:
        dic['retorno'] = {'erro': True, 'mensagem': "Usuário ou senha inválidos."}
  else:
    dic['retorno'] = {'erro': True, 'mensagem': "Dados inválidos"}

  dic['form'] = form

  return render(request, 'login.html', dic)

def realiza_logout(request):
  logout(request)
  return redirect('/')


def cadastro(request):
  dic = {}
  form = FormCadastro()

  if request.method == 'POST':
    form = FormCadastro(request.POST)
    if form.is_valid():
      dados = {
        'username': form.cleaned_data['username'],
        'password': form.cleaned_data['password'],
        'first_name': form.cleaned_data['first_name'],
        'last_name': form.cleaned_data['last_name'],
        'email': form.cleaned_data['email']
      }

      dic['retorno'] = cria_usuario(dados)
      dic['form'] = FormCadastro()

      return render(request, 'cadastro.html', dic)

  dic['form'] = form
  dic['cadastrar'] = True

  return render(request, 'cadastro.html', dic)

@login_required
def collections(request):

  if request.method == 'GET':
    if 'colecao' in request.GET.keys():
      dados = {
        'colecao': request.GET['colecao'],
        'user': request.user
      }

      dic = {
        'colecao': dados['colecao'],
        'imagens': busca_imagens(request.user, dados['colecao'])
      }

      modal = render(request, 'modais.html', dic).content

      retorno = json.dumps({'modal': modal.decode("utf-8")}, default=DjangoJSONEncoder().default)

      return HttpResponse(retorno)

      # return render(request, 'modais.html', dic)

  colecoes_user = colecoes(request.user)
  favoritos_user = favoritos(request.user)

  dic = {
    'colecoes': colecoes_user,
    'favoritos': favoritos_user
  }

  return render(request, 'collections.html', dic)