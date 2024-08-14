from datetime import datetime
from django.db import models
from .utils import calcular_total

class Categoria(models.Model):
  choice_tipo = (
    ('E', 'ENTRADA'), 
    ('S', 'SAIDA'),
    ('M', 'MENSAL')
  )

  categoria = models.CharField(max_length=50)
  tipo = models.CharField(max_length=1, choices=choice_tipo)
  valor_planejamento = models.FloatField(default=0)

  def __str__(self):
    return self.categoria
  
  def valor_gasto_saida(self):  # Soma o valor total gasto nas movimentações de saída.
    from contas.models import Movimentacao
    valores = Movimentacao.objects.filter(categoria__id=self.id).filter(data__month=datetime.now().month).filter(tipo='S')
    return calcular_total(valores, 'valor') # calcular_total(objetos, campo)
  
  def valor_gasto_mensal(self): # Soma o valor total gasto nas contas mensais.
    from contas.models import ContasMensais
    valores = ContasMensais.objects.filter(categoria__id=self.id).filter(dia_vencimento__month=datetime.now().month).filter(conta_paga=True)
    return calcular_total(valores, 'valor') # calcular_total(objetos, campo)
  
  # def saidas(self): # Retorna somente as movimentações de saída.
  #   from contas.models import Movimentacao
  #   saidas = Movimentacao.objects.filter(categoria__id=self.id).filter(tipo='S')
  #   return saidas
  
  def percentual_gasto_saida(self): # Barra de progresso 'movimentação'.
    if self.valor_planejamento:
      return int((self.valor_gasto_saida() * 100) / self.valor_planejamento)
    return 0
  
  def percentual_gasto_mensal(self):  # Barra de progresso 'conta mensal'.
    if self.valor_planejamento:
      return int((self.valor_gasto_mensal() * 100) / self.valor_planejamento)
    return 0
  

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
  valor = models.FloatField(blank=True, null=True)
  icone = models.ImageField(upload_to='icones')

  def __str__(self):
    return self.nome
  
  