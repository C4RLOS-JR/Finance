from django.db import models
from perfil.models import Categoria, Conta

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


class ContaPagar(models.Model):
  titulo = models.CharField(max_length=50)
  categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
  descricao = models.TextField(blank=True, null=True)
  valor = models.FloatField(blank=True, null=True)
  dia_pagamento = models.IntegerField()

  def __str__(self):
    return self.titulo
  
  class Meta:
    verbose_name = "Contas a Pagar"
    verbose_name_plural = "Contas a Pagar"
  

class ContaPaga(models.Model):
  conta = models.ForeignKey(ContaPagar, on_delete=models.DO_NOTHING)
  valor = models.FloatField(default=0)
  dia_pagamento = models.DateField()

  def __str__(self):
    return self.conta.titulo

  class Meta:
    verbose_name = "Contas Pagas"
    verbose_name_plural = "Contas Pagas"
