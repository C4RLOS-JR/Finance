from django.urls import path
from . import views

urlpatterns = [
    path('movimentacao/<str:tipo_movimentacao>', views.movimentacao, name='movimentacao'),
    path('definir_contas/', views.definir_contas, name='definir_contas'),
    path('ver_contas/', views.ver_contas, name='ver_contas'),
    path('pagar_contas/<int:conta_id>', views.pagar_contas, name='pagar_contas'),
    path('transferir/', views.transferir, name='transferir'),
]