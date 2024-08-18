from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from perfil.models import Conta, Categoria
from contas.models import Movimentacao, ContasMensais, Transferencias
from datetime import datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO
    
def ver_extrato(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  movimentacao = Movimentacao.objects.all()
  contas_mensais = ContasMensais.objects.all()

  id_conta = request.POST.get('id_conta')  # Filtrar pela conta
  id_categoria = request.POST.get('id_categoria')  # Filtrar pela categoria
  mes = request.POST.get('mes')
  saidas = []

  if not mes:
    movimentacao = movimentacao.filter(data__month=datetime.now().month) # Filtra e traz os valores do mês atual.
    contas_mensais = contas_mensais.filter(pago_dia__month=datetime.now().month).filter(conta_paga=True) # Filtra e traz os valores do mês atual e contas pagas.
  else:
    data = mes.split('-')
    movimentacao = movimentacao.filter(data__month=data[1]).filter(data__year=data[0])  # Filtra e traz os valores do mês selecionado.
    contas_mensais = contas_mensais.filter(pago_dia__month=data[1]).filter(pago_dia__year=data[0]).filter(conta_paga=True) # Filtra e traz os valores do mês selecionado e contas pagas.

  if id_conta:
    movimentacao = movimentacao.filter(conta_pagamento__id=id_conta)
    contas_mensais = contas_mensais.filter(conta_pagamento__id=id_conta)
  if id_categoria:
    movimentacao = movimentacao.filter(categoria__id=id_categoria)
    contas_mensais = contas_mensais.filter(categoria__id=id_categoria)

  for saida in movimentacao:
    saidas += [{'conta': saida.conta_pagamento, 'titulo': saida.titulo, 'categoria': saida.categoria, 'data': saida.data, 'tipo': saida.tipo, 'valor': saida.valor},]
  for saida in contas_mensais:
    saidas += [{'conta': saida.conta_pagamento, 'titulo': saida.titulo, 'categoria': saida.categoria, 'data': saida.pago_dia, 'tipo': saida.categoria.tipo, 'valor': saida.valor},]

  if saidas:
    saidas = sorted(saidas, key=lambda x: x['data'])  # Ordenando a lista de saídas pela data de pagamento.
    saidas.reverse()

  return render(request, 'extrato.html', {
    'contas': contas,
    'categorias': categorias,
    'saidas': saidas})


def extrato_transferencias(request):
  transferencias = Transferencias.objects.filter(data__month=datetime.now().month)
  transferencias.reverse()
  return render(request, 'extrato_transferencias.html', {'transferencias': transferencias})


def exportar_pdf(request):
  movimentacao = Movimentacao.objects.filter(data__month=datetime.now().month) # Filtra e traz as saídas e entradas do mês atual.
  contas_mensais = ContasMensais.objects.filter(pago_dia__month=datetime.now().month).filter(conta_paga=True) # Filtra e traz as contas mensais do mês atual.
  data = datetime.now().date()
  mes = request.POST.get('mes')
  saidas = []

  print(mes)

  for saida in movimentacao:
    saidas += [{'conta': saida.conta_pagamento, 'titulo': saida.titulo, 'categoria': saida.categoria, 'data': saida.data, 'tipo': saida.tipo, 'valor': saida.valor},]
  for saida in contas_mensais:
    saidas += [{'conta': saida.conta_pagamento, 'titulo': saida.titulo, 'categoria': saida.categoria, 'data': saida.pago_dia, 'tipo': saida.categoria.tipo, 'valor': saida.valor},]

  saidas = sorted(saidas, key=lambda x: x['data'])  # Ordenando a lista de saídas pela data de pagamento.

  path_template = os.path.join(settings.BASE_DIR, 'templates/partials/gerar_extrato.html')  # Salva o caminho de HTML na variável.
  template_render = render_to_string(path_template, {'saidas': saidas, 'data': data}) # Converte o HTML em string.

  path_output = BytesIO() # Cria uma instância em memória.
  HTML(string=template_render).write_pdf(path_output) # Escreve o HTML e salva na instância da memória.
  path_output.seek(0) # Volta o ponteiro para o início do arquivo.

  # Envia o arquivo para o usuário em PDF.
  return FileResponse(path_output, filename=f'extrato_{datetime.now().month}-{datetime.now().year}.pdf')
