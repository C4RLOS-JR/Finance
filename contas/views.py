from datetime import datetime
from django.shortcuts import render, redirect
from perfil.models import Categoria, Conta
from .models import ContasMensais
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
    valor = request.POST.get('valor')
    categoria = request.POST.get('categoria')
    descricao = request.POST.get('descricao')
    data = request.POST.get('data')
    id_conta = request.POST.get('id_conta')
    valor = valor.replace(',', '.')

    if (len(valor.strip())==0) or (len(descricao.strip())==0) or (len(data)==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect(f'../movimentacao/{tipo_movimentacao}')
    
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
        tipo = tipo_movimentacao)
      novo_valor.save()

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
      return redirect(f'../movimentacao/{tipo_movimentacao}')
    except:
      messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
      return redirect(f'../movimentacao/{tipo_movimentacao}')
    
def definir_contas(request):
  categorias = Categoria.objects.all()
  if request.method == 'GET':
    return render(request, 'definir_contas.html', {'categorias': categorias})
  
  elif request.method == 'POST':
    titulo = request.POST.get('titulo')
    categoria = request.POST.get('categoria')
    descricao = request.POST.get('descricao')
    valor = request.POST.get('valor')
    dia_vencimento = request.POST.get('dia_vencimento')

    if not valor:
      valor = None

    if (len(titulo.strip())==0) and (len(categoria.strip())==0) and (len(valor.strip())==0) and (len(dia_vencimento.strip())==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect('definir_contas')

    nova_conta = ContasMensais(
      titulo =titulo,
      categoria_id = categoria,
      descricao = descricao,
      valor = valor,
      dia_vencimento = dia_vencimento
    )
    nova_conta.save()

    messages.add_message(request, constants.SUCCESS, 'Nova conta criada com sucesso!')
    return redirect('home')

def ver_contas(request):
  MES_ATUAL = datetime.now().month
  DIA_ATUAL = datetime.now().day

  DATA_ATUAL = datetime.now()

  # pagas = ContaPaga.objects.filter(pago_dia__month=MES_ATUAL).values('conta')  # A função "values('conta')" trás o valor do campo passado como parametro.
  contas = ContasMensais.objects.all().order_by('dia_vencimento')
  contas_pagas = contas.filter(conta_paga=True)
  contas_vencidas = contas.filter(dia_vencimento__lt=DATA_ATUAL).exclude(id__in=contas_pagas)  # Filtra pelas contas que tem o dia de pagamento menor que o dia atual e que seu "id" não esteja em "contas_pagas".
  contas_proximas_vencimento = contas.filter(dia_vencimento__gte=DATA_ATUAL).filter(dia_vencimento__day__lte=DIA_ATUAL+5).exclude(id__in=contas_pagas)
  contas_restantes = contas.exclude(id__in=contas_pagas).exclude(id__in=contas_vencidas).exclude(id__in=contas_proximas_vencimento)

  return render(request, 'ver_contas.html', {
    'contas_pagas': contas_pagas,
    'contas_vencidas': contas_vencidas,
    'contas_proximas_vencimento': contas_proximas_vencimento,
    'contas_restantes': contas_restantes,
    'hoje': DATA_ATUAL
    })

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
    valor = valor.replace(',', '.')

    if (len(valor.strip())==0) or (len(dia_pagamento.strip())==0) or (len(conta_pagamento_id.strip())==0):
      messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
      return redirect(f'../pagar_contas/{conta_id}')
  
    conta = Conta.objects.get(id=conta_pagamento_id)
    conta.valor -= float(valor)
    
    if conta.valor < 0:
      messages.add_message(request, constants.ERROR, f'A conta "{conta.nome}" não tem saldo suficienta para realizar esse pagamento, escolha outra conta!')
      return redirect(f'../pagar_contas/{conta_id}')
    conta.save()

    pagar_conta.conta_paga = True
    pagar_conta.pago_dia = dia_pagamento
    pagar_conta.conta_pagamento = conta
    pagar_conta.save()

    messages.add_message(request, constants.SUCCESS, f'A conta mensal "{pagar_conta.titulo}" foi paga usando a conta do(a) {conta.nome}!')
    return redirect('ver_contas')
