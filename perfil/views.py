from django.shortcuts import render
from django.http import HttpResponse

def home(request):
  return render(request, 'home.html')

def gerenciar(request):
  return render(request, 'gerenciar.html')
  
def cadastrar_banco(request):
  nome = request.POST.get('nome')
  banco = request.POST.get('banco')
  tipo = request.POST.get('tipo')
  valor = request.POST.get('valor')
  icone = request.FILES.get('icone')

  if (len(nome)==0) or (len(banco)==0) or (len(valor)==0) or (icone==None):
    return HttpResponse('Preencha todos os campos')
  
  return HttpResponse(f'{nome} - {banco} - {tipo} - {valor}')
