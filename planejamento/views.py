from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from contas.models import Categoria
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import constants
from django.contrib import messages
import json

def definir_planejamento(request):
  categorias = Categoria.objects.all()
  return render(request, 'definir_planejamento.html', {'categorias': categorias})

@csrf_exempt
def modificar_valor_planejamento(request, id):
  novo_valor = json.load(request)['novo_valor'].replace(',', '.')
  categoria = Categoria.objects.get(id=id)

  if float(categoria.valor_planejamento) != float(novo_valor):
    categoria.valor_planejamento = novo_valor
    categoria.save()

    messages.add_message(request, constants.SUCCESS, f'O valor do planejamento "{categoria}" alterado com sucesso!')
    return JsonResponse({'status': 'Sucesso'})
  
  messages.add_message(request, constants.ERROR, f'O valor do planejamento "{categoria}" não foi alterado!')
  return JsonResponse({'status': 'Mantido'})


