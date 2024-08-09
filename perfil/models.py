from datetime import datetime
from django.db import models
from .utils import calcular_total

class Categoria(models.Model):
  categoria = models.CharField(max_length=50)
  essencial = models.BooleanField(default=False)
  valor_planejamento = models.IntegerField(default=0)

  def __str__(self):
    return self.categoria
  
  def valor_gasto(self):  # Soma o valor total gasto nas movimentações de saída.
    from contas.models import Valores
    valores = Valores.objects.filter(categoria__id=self.id).filter(data__month=datetime.now().month).filter(tipo='S')
    return calcular_total(valores, 'valor') # calcular_total(objetos, campo)
  
  def saidas(self): # Retorna somente as movimentações de saída.
    from contas.models import Valores
    saidas = Valores.objects.filter(categoria__id=self.id).filter(tipo='S')
    return saidas


class Conta(models.Model):
  banco_choices = (
    ('NU', 'NuBank'),
    ('CE', 'Caixa Econômica'),
    ('MP', 'Mercado Pago')
  )

  tipo_choices = (
    ('pf', 'Pessoa Física'),
    ('pj', 'Pesssoa Jurídica')
  )

  nome = models.CharField(max_length=50)
  banco = models.CharField(max_length=2, choices=banco_choices)
  tipo = models.CharField(max_length=2, choices=tipo_choices)
  valor = models.FloatField()
  icone = models.ImageField(upload_to='icones')

  def __str__(self):
    return self.nome
  
  