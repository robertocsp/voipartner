from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import *

# Create your views here.

def home_nao_logada(request):
    return render(request, 'views/home_nao_logada.html')

@login_required(login_url='/login')
def home_logada(request):
    return render(request, 'views/home_logada.html')

def cadastro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('email')  # o email é o username
            raw_password = form.cleaned_data.get('password1')

            form.save(username,raw_password)

            return redirect('home_logada')
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
                return redirect('home_logada')

            else:
                return redirect('home_nao_logada')
    else:
        form = LoginForm()
    return render(request, 'views/login.html', {'form': form})


def my_logout(request):
    logout(request)
    return redirect('home_nao_logada')



@login_required(login_url='/login')
def contratos_usuario(request):
    usuario = Usuario.objects.get(user=request.user)

    contratos_em_vigor = Contrato.objects.filter(usuario=usuario,status=2)
    contratos_pgto_pendente = Contrato.objects.filter(usuario=usuario, status=1)
    context = {
        'usuario': usuario,
        'contratos_em_vigor': contratos_em_vigor,
        'contratos_pgto_pendente': contratos_pgto_pendente,
    }

    return render(request, "views/contratos_usuario.html", context)


@login_required(login_url='/login')
def contrato(request, contrato_id):
    usuario = Usuario.objects.get(user=request.user)
    contrato = Contrato.objects.get(pk=contrato_id)
    context = {
        'usuario': usuario,
        'contrato' : contrato,
    }

    return render(request, "views/contrato.html", context)

def testeForm(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TesteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return redirect('home_logada')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = TesteForm()

    return render(request, 'views/testeform.html', {'form': form})

