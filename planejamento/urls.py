from django.urls import path
from . import views

urlpatterns = [
    path('definir_planejamento/', views.definir_planejamento, name='definir_planejamento'),
    path('modificar_valor_planejamento/<int:id>', views.modificar_valor_planejamento, name='modificar_valor_planejamento'),
]
