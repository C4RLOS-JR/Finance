from django.shortcuts import render, redirect
from django.http import HttpResponse
from contas.models import Categoria

def definir_planejamento(request):
  categorias = Categoria.objects.all()
  return render(request, 'definir_planejamento.html', {'categorias': categorias})

def modificar_valor_planejamento(request, id):
  categoria = Categoria.objects.get(id=id)

  return HttpResponse(categoria)
