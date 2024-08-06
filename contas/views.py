from curses.ascii import HT
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from perfil.models import Conta, Categoria
from .models import Valores
from django.contrib.messages import constants
from django.contrib import messages
from datetime import date, datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO

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
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  id_conta = request.GET.get('id_conta')
  id_categoria = request.GET.get('id_categoria')
  periodo = request.GET.get('periodo')

  movimentacao = Valores.objects.filter(data__month=datetime.now().month) # Filtra e traz os valores do mês atual.

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
  movimentacao = Valores.objects.filter(data__month=datetime.now().month) # Filtra e traz os valores do mês atual.
  path_template = os.path.join(settings.BASE_DIR, 'templates/partials/gerar_extrato.html')  # Salva o caminho de HTML na variável.
  template_render = render_to_string(path_template, {'movimentacao': movimentacao}) # Converte o HTML em string.

  path_output = BytesIO() # Cria uma instância em memória.
  HTML(string=template_render).write_pdf(path_output) # Escreve o HTML e salva na instância da memória.
  path_output.seek(0) # Volta o ponteiro para o início do arquivo.

  # Envia o arquivo para o usuário em PDF.
  return FileResponse(path_output, filename=f'extrato_{datetime.now().month}-{datetime.now().year}.pdf')
