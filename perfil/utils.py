def calcular_total(objetos, campo):
  total = 0
  for objeto in objetos:
    total += getattr(objeto, campo)

  return total
