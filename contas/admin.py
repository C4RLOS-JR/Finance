from django.contrib import admin
from .models import Movimentacao, ContasMensais, Transferencias

admin.site.register(Movimentacao)
admin.site.register(ContasMensais)
admin.site.register(Transferencias)
