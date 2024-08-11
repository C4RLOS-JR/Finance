from datetime import datetime
from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from .models import ContaPagar, ContaPaga
from .models import Movimentacao
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
      
      novo_valor = Movimentacao(
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
    
def definir_contas(request):
  categorias = Categoria.objects.all()
  if request.method == 'GET':
    return render(request, 'definir_contas.html', {'categorias': categorias})
  
  elif request.method == 'POST':
    titulo = request.POST.get('titulo')
    categoria = request.POST.get('categoria')
    descricao = request.POST.get('descricao')
    valor = request.POST.get('valor')
    dia_pagamento = request.POST.get('dia_pagamento')

    if (len(titulo.strip())==0) and (len(categoria.strip())==0) and (len(valor.strip())==0) and (len(dia_pagamento.strip())==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect('definir_contas')

    nova_conta = ContaPagar(
      titulo =titulo,
      categoria_id = categoria,
      descricao = descricao,
      valor = valor,
      dia_pagamento = dia_pagamento
    )
    nova_conta.save()

    messages.add_message(request, constants.SUCCESS, 'Nova conta criada com sucesso!')
    return redirect('home')

def ver_contas(request):
  MES_ATUAL = datetime.now().month
  DIA_ATUAL = datetime.now().day

  pagas = ContaPaga.objects.filter(dia_pagamento__month=MES_ATUAL).values('conta')  # A função "values('conta')" trás o valor do campo passado como parametro.
  contas = ContaPagar.objects.all().order_by('dia_pagamento')
  contas_pagas = contas.filter(id__in=pagas)
  contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=pagas)  # Filtra pelas contas que tem o dia de pagamento menor que o dia atual e que seu "id" não esteja em "contas_pagas".
  contas_proximas_vencimento = contas.filter(dia_pagamento__gt=DIA_ATUAL).filter(dia_pagamento__lte=DIA_ATUAL+5).exclude(id__in=pagas)
  contas_restantes = contas.exclude(id__in=pagas).exclude(id__in=contas_vencidas).exclude(id__in=contas_proximas_vencimento)


  return render(request, 'ver_contas.html', {
    'contas_pagas': contas_pagas,
    'contas_vencidas': contas_vencidas,
    'contas_proximas_vencimento': contas_proximas_vencimento,
    'contas_restantes': contas_restantes
    })

def pagar_contas(request, conta_id):
  conta_paga = ContaPaga(
    conta_id = conta_id,
    dia_pagamento = datetime.now()
  )
  conta_paga.save()

  return redirect('ver_contas')
