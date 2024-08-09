from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Conta, Categoria
from contas.models import Movimentacao
from django.contrib.messages import constants
from django.contrib import messages
from .utils import calcular_total
from datetime import datetime

def home(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  saidas = Movimentacao.objects.filter(data__month=datetime.now().month).filter(tipo='S')
  valor_total_contas = calcular_total(contas, 'valor')
  valor_total_saidas = calcular_total(saidas, 'valor')
  valor_total_planejamento = calcular_total(categorias, 'valor_planejamento')
  percentual_planejamento = int((valor_total_saidas * 100) / valor_total_planejamento)


  return render(request, 'home.html',{
    'contas': contas,
    'valor_total_contas': valor_total_contas,
    'categorias': categorias,
    'valor_total_saidas': valor_total_saidas,
    'valor_total_planejamento': valor_total_planejamento,
    'percentual_planejamento': percentual_planejamento })

def gerenciar(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  valor_total = calcular_total(contas, 'valor') # calcular_total(objetos, campo)

  return render(request, 'gerenciar.html',{
    'contas': contas,
    'valor_total': valor_total,
    'categorias': categorias })
  
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
  essencial = bool(request.POST.get('essencial'))

  if len(categoria.strip()) == 0:
    messages.add_message(request, constants.ERROR, 'O campo categoria não pode ficar em branco!')
    return redirect('gerenciar')

  try:
    nova_categoria = Categoria(
      categoria = categoria,
      essencial = essencial
    )
    nova_categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria adicionada com sucesso!')
    return redirect('gerenciar')
  except:
    messages.add_message(request, constants.ERROR, 'Algo deu errado...tente novamente ou fale com um administrador!')
    return redirect('gerenciar')

def update_categoria(request, categoria_id):
  categoria = Categoria.objects.get(id=categoria_id)

  categoria.essencial = not categoria.essencial
  categoria.save()

  return redirect('gerenciar')
