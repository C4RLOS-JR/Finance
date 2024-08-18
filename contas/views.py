from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from .models import ContasMensais, Transferencias
from .models import Movimentacao
from django.contrib.messages import constants
from django.contrib import messages


def movimentacao(request, tipo_movimentacao):
  if request.method == 'GET':
    contas = Conta.objects.all()
    categorias = Categoria.objects.filter(tipo=tipo_movimentacao)

    return render(request, 'movimentacao.html', {
      'contas': contas,
      'categorias': categorias,
      'tipo_movimentacao': tipo_movimentacao})
  
  if request.method == 'POST':
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')
    categoria = request.POST.get('categoria')
    data = request.POST.get('data')
    id_conta = request.POST.get('id_conta')
    valor = valor.replace(',', '.')

    if (len(titulo.strip())==0) or (len(valor.strip())==0) or (len(data)==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect(f'../movimentacao/{tipo_movimentacao}')

    try:
      conta = Conta.objects.get(id=id_conta)

      if tipo_movimentacao == 'S':
        if conta.valor - float(valor) < 0:
          messages.add_message(request, constants.ERROR, 'Essa conta não tem saldo suficiente para essa despesa...escolha outra conta!')
          return redirect(f'../movimentacao/{tipo_movimentacao}')
        conta.valor -= float(valor)
        messages.add_message(request, constants.SUCCESS, 'Saída cadastrada com sucesso!')
      else:
        conta.valor += float(valor)
        messages.add_message(request, constants.SUCCESS, 'Entrada cadastrada com sucesso!')
      conta.save()

      novo_valor = Movimentacao(
        titulo = titulo,
        valor = valor,
        categoria_id = categoria,
        data = data,
        conta_pagamento_id = id_conta,
        tipo = tipo_movimentacao)
      novo_valor.save()

      return redirect('home')
    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
      return redirect(f'../movimentacao/{tipo_movimentacao}')


def contas_mensais(request):
  if request.method == 'GET':
    DATA_ATUAL = datetime.now()

    categorias = Categoria.objects.all()
    contas = ContasMensais.objects.all().order_by('dia_vencimento')
    contas_pagas = contas.filter(conta_paga=True)
    contas_vencidas = contas.filter(dia_vencimento__lt=DATA_ATUAL).exclude(id__in=contas_pagas)  # Filtra pelas contas que tem o dia de pagamento menor que o dia atual e que seu "id" não esteja em "contas_pagas".
    contas_proximas_vencimento = contas.filter(dia_vencimento__gte=DATA_ATUAL).filter(dia_vencimento__day__lte=DATA_ATUAL.day+5).exclude(id__in=contas_pagas)
    contas_restantes = contas.exclude(id__in=contas_pagas).exclude(id__in=contas_vencidas).exclude(id__in=contas_proximas_vencimento)

    return render(request, 'contas_mensais.html', {
      'categorias': categorias,
      'contas_pagas': contas_pagas,
      'contas_vencidas': contas_vencidas,
      'contas_proximas_vencimento': contas_proximas_vencimento,
      'contas_restantes': contas_restantes,
      'hoje': DATA_ATUAL
      })
  
  elif request.method == 'POST':
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')
    categoria = request.POST.get('categoria')
    dia_vencimento = request.POST.get('dia_vencimento')
    valor = valor.replace(',', '.')

    if not valor:
      valor = None

    if (len(titulo.strip())==0) or (len(categoria.strip())==0) or (len(valor.strip())==0) or (len(dia_vencimento.strip())==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect('contas_mensais')

    try:
      nova_conta = ContasMensais(
        titulo =titulo,
        valor = valor,
        categoria_id = categoria,
        dia_vencimento = dia_vencimento
      )
      nova_conta.save()
      messages.add_message(request, constants.SUCCESS, 'Nova conta criada com sucesso!')

    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
      
    return redirect('contas_mensais')


def pagar_contas(request, conta_id):
  pagar_conta = ContasMensais.objects.get(id=conta_id)
  contas = Conta.objects.all()
  if request.method == 'GET':
    return render(request, 'pagar_conta.html', {
      'pagar_conta':pagar_conta,
      'contas': contas,
      'conta_id': conta_id})

  elif request.method == 'POST':
    conta_pagamento_id = request.POST.get('conta_pagamento_id')
    dia_pagamento = request.POST.get('data')
    valor = request.POST.get('valor')
    
    if valor:
      valor = valor.replace(',', '.')
    else:
      valor = pagar_conta.valor

    if not valor or (len(dia_pagamento.strip())==0) or (len(conta_pagamento_id.strip())==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect(f'../pagar_contas/{conta_id}')
  
    conta = Conta.objects.get(id=conta_pagamento_id)
    conta.valor -= float(valor)
    
    if conta.valor < 0:
      messages.add_message(request, constants.ERROR, f'A conta "{conta.nome}" não tem saldo suficienta para realizar esse pagamento, escolha outra conta!')
      return redirect(f'../pagar_contas/{conta_id}')
    conta.save()

    pagar_conta.valor = valor
    pagar_conta.conta_paga = True
    pagar_conta.pago_dia = dia_pagamento
    pagar_conta.conta_pagamento = conta
    pagar_conta.save()

    messages.add_message(request, constants.SUCCESS, f'A conta mensal "{pagar_conta.titulo}" foi paga usando a conta "{conta.nome}"!')
    return redirect('contas_mensais')
  

def transferir(request):
  contas = Conta.objects.all()

  if request.method == 'GET':
    return render(request, 'transferir.html', {'contas': contas})
  
  elif request.method == 'POST':
    id_conta_partida = request.POST.get('id_conta_partida')
    id_conta_destino = request.POST.get('id_conta_destino')
    valor = request.POST.get('valor')
    valor = valor.replace(',', '.')
    data = request.POST.get('data')

    if (len(id_conta_partida.strip())==0) or (len(id_conta_destino.strip())==0) or (len(valor.strip())==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect('transferir')
    
    if id_conta_partida == id_conta_destino:
      messages.add_message(request, constants.ERROR, 'As contas precisam ser diferentes!')
      return redirect('transferir')
    
    try:
      transferencia = Transferencias(
        conta_partida_id = id_conta_partida,
        conta_destino_id = id_conta_destino,
        valor = valor,
        data = data
      )
      transferencia.save()

      conta_partida = contas.get(id=id_conta_partida)
      conta_partida.valor -= float(valor)
      conta_partida.save()

      conta_destino = contas.get(id=id_conta_destino)
      conta_destino.valor += float(valor)
      conta_destino.save()

      messages.add_message(request, constants.SUCCESS, 'Transferencia realizada com sucesso!')
      return redirect('home')
    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
      return redirect('transferir')
