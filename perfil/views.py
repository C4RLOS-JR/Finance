from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Conta

def home(request):
  return render(request, 'home.html')

def gerenciar(request):
  contas = Conta.objects.all()
  return render(request, 'gerenciar.html', {'contas': contas})
  
def cadastrar_banco(request):
  nome = request.POST.get('nome')
  banco = request.POST.get('banco')
  tipo = request.POST.get('tipo')
  valor = request.POST.get('valor')
  icone = request.FILES.get('icone')

  if (len(nome)==0) or (len(banco)==0) or (len(valor)==0):
    return HttpResponse('Preencha todos os campos')
  if not icone:
    icone = 'default/icon_bank.png'
    
  nova_conta = Conta(
    nome = nome,
    banco = banco,
    tipo = tipo,
    valor = valor,
    icone = icone
  )
  nova_conta.save()

  return redirect('gerenciar')

def excluir_banco(request, conta_id):
  conta = Conta.objects.get(id=conta_id)

  if not conta.icone == ('default/icon_bank.png'):
    conta.icone.delete()
  conta.delete()

  return redirect('gerenciar')
