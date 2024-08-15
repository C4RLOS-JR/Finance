from django.urls import path
from . import views

urlpatterns = [
    path('ver_extrato/', views.ver_extrato, name='ver_extrato'),
    path('extrato_transferencias/', views.extrato_transferencias, name='extrato_transferencias'),
    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),
]
