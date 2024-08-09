from email import message
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from contas.models import Categoria, Valores
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import constants
from django.contrib import messages
import json

def definir_planejamento(request):
  categorias = Categoria.objects.all()
  return render(request, 'definir_planejamento.html', {'categorias': categorias})

@csrf_exempt
def modificar_valor_planejamento(request, id):
  novo_valor = json.load(request)['novo_valor']
  categoria = Categoria.objects.get(id=id)

  if str(categoria.valor_planejamento) != novo_valor:
    categoria.valor_planejamento = novo_valor
    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Valor do planejamento alterado com sucesso!')
    return JsonResponse({'status': 'Sucesso'})
  return JsonResponse({'status': 'Mantido'})

def ver_planejamento(request):
  categorias = Categoria.objects.all()
  valores = Valores.objects.all()

  return render(request, 'ver_planejamento.html', {'categorias': categorias, 'valores': valores})

