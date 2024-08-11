from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from perfil.models import Conta, Categoria
from contas.models import Movimentacao
from datetime import datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO
    
def ver_extrato(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  id_conta = request.GET.get('id_conta')
  id_categoria = request.GET.get('id_categoria')
  periodo = request.GET.get('periodo')

  movimentacao = Movimentacao.objects.filter(data__month=datetime.now().month) # Filtra e traz os valores do mês atual.

  if id_conta:
    movimentacao = movimentacao.filter(conta__id=id_conta)
  if id_categoria:
    movimentacao = movimentacao.filter(categoria__id=id_categoria)

  # Fazer  filtrar por período.
  # if periodo:
  #   periodo = datetime.now().day - int(periodo)
  #   if periodo < 0:
  #     periodo = 1
  #   movimentacao = movimentacao.filter()
  
  return render(request, 'extrato.html', {'contas': contas, 'categorias': categorias, 'movimentacao': movimentacao})

def exportar_pdf(request):
  movimentacao = Movimentacao.objects.filter(data__month=datetime.now().month) # Filtra e traz os valores do mês atual.
  path_template = os.path.join(settings.BASE_DIR, 'templates/partials/gerar_extrato.html')  # Salva o caminho de HTML na variável.
  template_render = render_to_string(path_template, {'movimentacao': movimentacao}) # Converte o HTML em string.

  path_output = BytesIO() # Cria uma instância em memória.
  HTML(string=template_render).write_pdf(path_output) # Escreve o HTML e salva na instância da memória.
  path_output.seek(0) # Volta o ponteiro para o início do arquivo.

  # Envia o arquivo para o usuário em PDF.
  return FileResponse(path_output, filename=f'extrato_{datetime.now().month}-{datetime.now().year}.pdf')
