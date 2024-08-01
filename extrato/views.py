from django.shortcuts import render, redirect
from django.http import HttpResponse
from perfil.models import Conta, Categoria

def novo_valor(request):
  contas = Conta.objects.all()
  categorias = Categoria.objects.all()
  if request.method == 'GET':
    return render(request, 'novo_valor.html', {'contas': contas, 'categorias': categorias})
