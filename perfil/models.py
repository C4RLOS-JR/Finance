from django.db import models
from django.forms import CharField

class Categoria(models.Model):
  categoria = models.CharField(max_length=50)
  essencial = models.BooleanField(default=False)
  valor_planejamento = models.IntegerField(default=0)

  def __str__(self):
    return self.categoria


class Conta(models.Model):
  nome = models.CharField(max_length=50)