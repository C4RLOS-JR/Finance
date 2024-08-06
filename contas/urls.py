from django.urls import path
from . import views

urlpatterns = [
    path('movimentacao/', views.movimentacao, name='movimentacao'),
    path('extrato/', views.extrato, name='extrato'),
    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
]
