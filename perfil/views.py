from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Conta, Categoria
from contas.models import Movimentacao, ContasMensais
from django.contrib.messages import constants
from django.contrib import messages
from .utils import calcular_total
from datetime import date, datetime


def home(request):
  DATA_ATUAL=datetime.now()
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  movimentacao = Movimentacao.objects.filter(data__month=DATA_ATUAL.month)
  contas_mensais = ContasMensais.objects.filter(dia_vencimento__month=DATA_ATUAL.month).filter(conta_paga=True)
  contas_mensais_nao_pagas = ContasMensais.objects.filter(dia_vencimento__month=DATA_ATUAL.month).filter(conta_paga=False)
  
  vencidas = contas_mensais_nao_pagas.filter(dia_vencimento__day__lt=DATA_ATUAL.day)
  proximas_vencimento = contas_mensais_nao_pagas.filter(dia_vencimento__day__gt=DATA_ATUAL.day).filter(dia_vencimento__day__lte=DATA_ATUAL.day+5)
  vence_hoje = contas_mensais_nao_pagas.filter(dia_vencimento=DATA_ATUAL)
  outras = contas_mensais_nao_pagas.exclude(id__in=vencidas).exclude(id__in=proximas_vencimento).exclude(id__in=vence_hoje)


  print(vencidas)
  print(proximas_vencimento)
  print(vence_hoje)


  entradas = movimentacao.filter(tipo='E')
  saidas = movimentacao.filter(tipo='S')
  total_entradas = calcular_total(entradas, 'valor')  # Receita mensal
  total_saidas = calcular_total(saidas, 'valor')  # Despesa mensal
  total_mensais = calcular_total(contas_mensais, 'valor')  # Despesa mensal
  total_despesas = total_saidas + total_mensais  # Despesa mensal
  valor_total_contas = calcular_total(contas, 'valor')  # Saldo total
  valor_total_planejamento = calcular_total(categorias, 'valor_planejamento')

  planejamento_total = 0
  percentual_planejamento_total = 0

  for saida in saidas:
    if saida.categoria.valor_planejamento != 0: # Acrescenta ao 'planejamento_total' o valor total de saída se o 'valor_planejamento' for diferente de 0.
      planejamento_total += saida.valor

  for conta_mensal in contas_mensais:
    if conta_mensal.categoria.valor_planejamento != 0:  # Acrescenta ao 'planejamento_total' o valor total pago das contas mensais se o 'valor_planejamento' for diferente de 0.
      planejamento_total += conta_mensal.valor

  if planejamento_total and valor_total_planejamento:
    percentual_planejamento_total = int((planejamento_total * 100) / valor_total_planejamento)

  return render(request, 'home.html',{
    'contas': contas,
    'categorias': categorias,
    'vencidas': vencidas.count(),
    'proximas_vencimento':proximas_vencimento.count(),
    'vence_hoje': vence_hoje.count(),
    'outras': outras.count(),
    'total_saidas': total_saidas,
    'total_entradas': total_entradas,
    'total_despesas': total_despesas,
    'valor_total_contas': valor_total_contas,
    'valor_total_planejamento': valor_total_planejamento,
    'planejamento_total': planejamento_total,
    'percentual_planejamento_total': percentual_planejamento_total
    })
  

def gerenciar(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  valor_total = calcular_total(contas, 'valor') # calcular_total(objetos, campo)

  return render(request, 'gerenciar.html',{
    'contas': contas,
    'valor_total': valor_total,
    'categorias': categorias
    })

  
def cadastrar_banco(request):
  nome = request.POST.get('nome')
  banco = request.POST.get('banco')
  tipo = request.POST.get('tipo')
  valor = request.POST.get('valor')
  icone = request.FILES.get('icone')
  valor = valor.replace(',', '.')

  if (len(nome.strip()) == 0) or (len(banco) == 0) or (len(valor.strip()) == 0):
    messages.add_message(request, constants.ERROR, 'Preencha todos os campos!')
    return redirect('gerenciar')
  
  if not icone:
    icone = 'default/icon_bank.png'

  try:  
    conta = Conta(
      nome = nome,
      banco = banco,
      tipo = tipo,
      valor = valor,
      icone = icone)
    conta.save()

    messages.add_message(request, constants.SUCCESS, 'Conta adicionada com sucesso!')
    return redirect('gerenciar')
  except:
    messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
    return redirect('gerenciar')


def excluir_banco(request, conta_id):
  conta = Conta.objects.get(id=conta_id)

  if not conta.icone == ('default/icon_bank.png'):
    conta.icone.delete()
  conta.delete()

  messages.add_message(request, constants.SUCCESS, 'Conta excluída com sucesso!')
  return redirect('gerenciar')


def cadastrar_categoria(request):
  categoria = request.POST.get('categoria')
  tipo = request.POST.get('tipo')

  if len(categoria.strip()) == 0:
    messages.add_message(request, constants.ERROR, 'O campo categoria não pode ficar em branco!')
    return redirect('gerenciar')

  try:
    nova_categoria = Categoria(
      categoria = categoria,
      tipo = tipo
    )
    nova_categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria adicionada com sucesso!')
    return redirect('gerenciar')
  except:
    messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
    return redirect('gerenciar')


def dashboard(request):
  dados = {}

  categorias = Categoria.objects.all()
  for categoria in categorias:
    total = 0
    valores = Movimentacao.objects.filter(categoria=categoria)
    for gasto in valores:
      total += gasto.valor
    
    dados[categoria.categoria] = total

  return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})