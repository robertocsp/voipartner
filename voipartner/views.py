from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *

from django.http import HttpResponse
import os
from django.conf import settings
from django.contrib import messages


# Create your views here.

def home(request):
    return render(request, 'views/home.html')

def cadastro(request):
    if request.method == 'POST':

        if request.user.is_anonymous:
            form = UsuarioForm(request.POST)
        else:
            instance = get_object_or_404(Usuario, id=Usuario.get_usuario_by_user(request.user).id)
            form = UsuarioForm(request.POST or None, instance=instance)

        if form.is_valid():
            #Valida se a data de nascimento é maior que o dia de hoje

            data_nascimento = form.cleaned_data.get('data_nascimento')
            if data_nascimento > datetime.datetime.now().date():
                messages.error(request, "Data de nascimento maior que o dia de hoje, usuário não nasceu")
                return render(request, 'views/cadastro.html', {'form': form})

            username = form.cleaned_data.get('email')  # o email é o username
            raw_password = form.cleaned_data.get('password1')

            '''
            # Valida se email já existe - Essa função tem ir para o form, para testar o estado.
            
            if Usuario.objects.get(email=username):
                messages.error(request, "Email já cadastrado")
                return render(request, 'views/cadastro.html', {'form': form})
            '''

            form.save(username, raw_password)

            return redirect('my_login')

    elif request.user.is_anonymous is not True:
        instance = get_object_or_404(Usuario, id=Usuario.get_usuario_by_user(request.user).id)
        form = UsuarioForm(request.POST or None, instance=instance)
    else:
        form = UsuarioForm()
    return render(request, 'views/cadastro.html', {'form': form})

def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')  # o email é o username
            raw_password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=raw_password)
            if user is not None:
                login(request, user)
                request.session['nome_usuario'] = Usuario.get_nome_by_user(user)
                return redirect('home')

            else:
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'views/login.html', {'form': form})


def my_logout(request):
    logout(request)
    return redirect('home')

#PENDENTE.... TEM QUE FAZER ALGUM CONTROLE DE ACESSO PARA DOWNLOAD DOS ARQUIVOS
@login_required(login_url='/login')
def download(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
    #return HttpResponse("chegou no download: " + filename)


@login_required(login_url='/login')
def contratos_usuario(request):
    usuario = Usuario.objects.get(user=request.user)

    contratos_em_vigor = Contrato.objects.filter(usuario=usuario,status=4)
    contratos_pendentes = Contrato.objects.filter(Q(usuario=usuario) & (Q(status=1) | Q(status=2) | Q(status=3)))
    context = {
        'usuario': usuario,
        'contratos_em_vigor': contratos_em_vigor,
        'contratos_pendentes': contratos_pendentes,
    }

    return render(request, "views/contratos_usuario.html", context)

@login_required(login_url='/login')
def contratos_pendentes(request):
    usuario = Usuario.objects.get(user=request.user)

    contratos_pendentes = Contrato.objects.filter(Q(usuario=usuario) & (Q(status=1) | Q(status=2) | Q(status=3)))
    context = {
        'usuario': usuario,
        'contratos_pendentes': contratos_pendentes,
    }

    return render(request, "views/contratos_pendentes.html", context)

@login_required(login_url='/login')
def contratos_em_vigor(request):
    usuario = Usuario.objects.get(user=request.user)

    contratos_em_vigor = Contrato.objects.filter(usuario=usuario,status=4)
    context = {
        'usuario': usuario,
        'contratos_em_vigor': contratos_em_vigor,
    }

    return render(request, "views/contratos_em_vigor.html", context)

@login_required(login_url='/login')
def contratos_encerrados(request):
    usuario = Usuario.objects.get(user=request.user)

    contratos_encerrados = Contrato.objects.filter(usuario=usuario,status=5)
    context = {
        'usuario': usuario,
        'contratos_encerrados': contratos_encerrados,
    }

    return render(request, "views/contratos_encerrados.html", context)

@login_required(login_url='/login')
def contrato(request, contrato_id):
    usuario = Usuario.objects.get(user=request.user)
    contrato = Contrato.objects.get(pk=contrato_id)
    context = {
        'usuario': usuario,
        'contrato' : contrato,
    }

    return render(request, "views/contrato.html", context)

@login_required(login_url='/login')
def contrato_pendente_detalhe(request, contrato_id):
    usuario = Usuario.objects.get(user=request.user)
    contrato = Contrato.objects.get(pk=contrato_id)
    contratos_pendentes = Contrato.objects.filter(Q(usuario=usuario) & (Q(status=1) | Q(status=2) | Q(status=3)))
    context = {
        'usuario': usuario,
        'contrato' : contrato,
        'contratos_pendentes': contratos_pendentes,
    }

    return render(request, "views/contrato_pendente_detalhe.html", context)

@login_required(login_url='/login')
def contrato_em_vigor_detalhe(request, contrato_id):
    usuario = Usuario.objects.get(user=request.user)
    contrato = Contrato.objects.get(pk=contrato_id)
    contratos_em_vigor = Contrato.objects.filter(usuario=usuario, status=4)
    context = {
        'usuario': usuario,
        'contrato': contrato,
        'contratos_em_vigor': contratos_em_vigor,
    }

    return render(request, "views/contrato_em_vigor_detalhe.html", context)

def contrato_encerrado_detalhe(request, contrato_id):
    usuario = Usuario.objects.get(user=request.user)
    contrato = Contrato.objects.get(pk=contrato_id)
    contratos_encerrados = Contrato.objects.filter(usuario=usuario, status=5)
    context = {
        'usuario': usuario,
        'contrato': contrato,
        'contratos_encerrados': contratos_encerrados,
    }

    return render(request, "views/contrato_encerrado_detalhe.html", context)

@login_required(login_url='/login')
def contrato_pendente_pagamento(request, contrato_id):
    if request.method == 'POST':

        contrato = Contrato.objects.get(pk=contrato_id)

        form = ContratoPendentePagamentoForm(request.POST, request.FILES, instance=contrato)

        if form.is_valid():

            form.save()
            #instance = form.save(commit=False)


            cotas_contratadas = form.cleaned_data.get('cotas_contratadas')
            #contrato.cotas_contratadas = cotas_contratadas


            #contrato.save()
            #form.save(username, raw_password)
        else:
            return HttpResponse("forulario nao foi valido")
        return redirect('contrato_pendente_detalhe', contrato_id=contrato.id)

    else:
        return HttpResponse("acesso não permitido")

@login_required(login_url='/login')
def dashboard(request):
    usuario = Usuario.get_usuario_by_user(request.user)
    context = {
        'usuario': usuario,

    }
    return render(request, "views/dashboard.html", context )


def testeForm(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TesteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('home')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = TesteForm()

    return render(request, 'views/testeform.html', {'form': form})

