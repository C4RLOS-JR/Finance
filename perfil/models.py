from django.db import models
from django.forms import CharField

class Categoria(models.Model):
  categoria = models.CharField(max_length=50)
  essencial = models.BooleanField(default=False)
  valor_planejamento = models.IntegerField(default=0)

  def __str__(self):
    return self.categoria


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
  
  