from django.db import models
from perfil.models import Categoria, Conta
from perfil.utils import calcular_total
from datetime import datetime

class Movimentacao(models.Model):
  choice_tipo = (
    ('E', 'ENTRADA'), 
    ('S', 'SAIDA')
  )

  titulo = models.CharField(max_length=50)
  valor = models.FloatField()
  categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
  data = models.DateField()
  conta_pagamento = models.ForeignKey(Conta, on_delete=models.DO_NOTHING)
  tipo = models.CharField(max_length=1, choices=choice_tipo)

  def __str__(self):
    movimentacao = lambda x: 'Entrada' if x == 'E' else 'Saída'
    return f'{self.titulo} ({movimentacao(self.tipo)})'
  
  class Meta:
    verbose_name = "Entradas/Saídas"
    verbose_name_plural = "Entradas/Saídas"


class ContasMensais(models.Model):
  titulo = models.CharField(max_length=50)
  valor = models.FloatField(blank=True, null=True)
  categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
  dia_vencimento = models.DateField()
  conta_paga = models.BooleanField(default=False)
  pago_dia = models.DateField(blank=True, null=True)
  conta_pagamento = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, blank=True, null=True)

  def __str__(self):
    return self.titulo
  
  class Meta:
    verbose_name = "Contas Mensais"
    verbose_name_plural = "Contas Mensais"


class Transferencias(models.Model):
  conta_partida = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, related_name='transferencias_partida')
  conta_destino = models.ForeignKey(Conta, on_delete=models.DO_NOTHING, related_name='transferencias_destino')
  valor = models.FloatField()
  data = models.DateField()

  def __str__(self):
    return f'{self.conta_partida} - {self.data}'
  
  class Meta:
    verbose_name = "Transferências"
    verbose_name_plural = "Transferências"