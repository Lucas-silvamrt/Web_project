from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('relatorio/', views.relatorio, name='relatorio'),
    path('gerenciar/', views.gerenciar, name='gerenciar'),
    path('gerenciar/novo/', views.novo_filme, name='novo_filme'),
    path('gerenciar/<int:pk>/editar/', views.editar_filme, name='editar_filme'),
    path('gerenciar/<int:pk>/excluir/', views.excluir_filme, name='excluir_filme'),
    path('gerenciar/importar/', views.importar_filme, name='importar_filme'),
    path('api/filmes/', views.api_filmes, name='api_filmes'),
    path('api/filmes/<int:pk>/', views.api_filme, name='api_filme'),
    path('filme/<int:pk>/', views.detalhe, name='detalhe'),
]
