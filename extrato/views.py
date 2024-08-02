from django.shortcuts import render, redirect
from django.http import HttpResponse
from perfil.models import Conta, Categoria
from .models import Valores
from django.contrib.messages import constants
from django.contrib import messages

def novo_valor(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  if request.method == 'GET':
    return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})
  
  if request.method == 'POST':
    valor = request.POST.get('valor')
    categoria = request.POST.get('categoria')
    descricao = request.POST.get('descricao')
    data = request.POST.get('data')
    conta = request.POST.get('conta')
    tipo = request.POST.get('tipo')

    if (len(valor.strip())==0) or (len(descricao.strip())==0) or (len(data)==0) or (len(tipo)==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect('novo_valor')
    
    if not valor.isnumeric():
      messages.add_message(request, constants.ERROR, 'O valor precisa ser um número!')
      return redirect('novo_valor')

    try:
      novo_valor = Valores(
        valor = valor,
        categoria = categoria,
        descricao = descricao,
        data = data,
        conta = conta,
        tipo = tipo)
      novo_valor.save()

      messages.add_message(request, constants.SUCCESS, 'Valor cadastrado com sucesso!')
      return redirect('novo_valor')
    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
      return redirect('novo_valor')
