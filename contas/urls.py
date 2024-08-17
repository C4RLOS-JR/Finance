from django.urls import path
from . import views

urlpatterns = [
    path('movimentacao/<str:tipo_movimentacao>', views.movimentacao, name='movimentacao'),
    path('contas_mensais/', views.contas_mensais, name='contas_mensais'),
    path('pagar_contas/<int:conta_id>', views.pagar_contas, name='pagar_contas'),
    path('transferir/', views.transferir, name='transferir'),
]