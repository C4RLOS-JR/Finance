from django.db import models
from perfil.models import Categoria, Conta
from perfil.utils import calcular_total
from datetime import datetime

class Movimentacao(models.Model):
  choice_tipo = (
    ('E', 'ENTRADA'), 
    ('S', 'SAIDA')
  )

  valor = models.FloatField()
  categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
  descricao = models.TextField()
  data = models.DateField()
  conta = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
  tipo = models.CharField(max_length=1, choices=choice_tipo)

  def __str__(self):
    return self.descricao
  
  class Meta:
    verbose_name = "Movimentação da conta"
    verbose_name_plural = "Movimentação da conta"


class ContasMensais(models.Model):
  titulo = models.CharField(max_length=50)
  categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
  descricao = models.TextField(blank=True, null=True)
  valor = models.FloatField(blank=True, null=True)
  dia_vencimento = models.DateField()
  conta_paga = models.BooleanField(default=False)
  pago_dia = models.DateField(blank=True, null=True)
  conta_pagamento = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, blank=True, null=True)

  def __str__(self):
    return self.titulo
  
  class Meta:
    verbose_name = "Contas Mensais"
    verbose_name_plural = "Contas Mensais"

  def pagas(self):
    valores = ContasMensais.objects.filter(categoria__id=self.id).filter(dia_vencimento__month=datetime.now().month).filter(conta_paga=True)
    return calcular_total(valores, 'valor')
  
