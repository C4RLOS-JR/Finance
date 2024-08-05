from django.shortcuts import render, redirect
from django.http import HttpResponse
from perfil.models import Conta, Categoria
from .models import Valores
from django.contrib.messages import constants
from django.contrib import messages

def movimentacao(request):
  if request.method == 'GET':
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'movimentacao.html', {'contas': contas, 'categorias': categorias})
  
  if request.method == 'POST':
    valor = request.POST.get('valor')
    categoria = request.POST.get('categoria')
    descricao = request.POST.get('descricao')
    data = request.POST.get('data')
    id_conta = request.POST.get('id_conta')
    tipo = request.POST.get('tipo')
    valor = valor.replace(',', '.')

    if (len(valor.strip())==0) or (len(descricao.strip())==0) or (len(data)==0) or (len(tipo)==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect('movimentacao')
    
    # if not valor.isnumeric():
    #   messages.add_message(request, constants.ERROR, 'O valor precisa ser um número!')
    #   return redirect('movimentacao')


    try:
      conta = Conta.objects.get(id=id_conta)
      
      novo_valor = Valores(
        valor = valor,
        categoria_id = categoria,
        descricao = descricao,
        data = data,
        conta_id = id_conta,
        tipo = tipo)
      novo_valor.save()

      if tipo == 'S':
        if conta.valor - float(valor) < 0:
          messages.add_message(request, constants.ERROR, 'Essa conta não tem saldo suficiente para essa despesa...escolha outra conta!')
          return redirect('movimentacao')
        conta.valor -= float(valor)
        messages.add_message(request, constants.SUCCESS, 'Saída cadastrada com sucesso!')
      else:
        conta.valor += float(valor)
        messages.add_message(request, constants.SUCCESS, 'Entrada cadastrada com sucesso!')
      conta.save()
      return redirect('movimentacao')
    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
      return redirect('movimentacao')
    
def extrato(request):
  if request.method == 'GET':
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    movimentacao = Valores.objects.all()
    
    return render(request, 'extrato.html', {'contas': contas, 'categorias': categorias, 'movimentacao': movimentacao})
