# blog/urls.py 

from django.urls import path 
from . import views # Importa as views do app blog 

app_name = 'blog' # Define o namespace para as URLs do app blog 

urlpatterns = [
    # URL para a lista de posts 
    path('', views.PostListView.as_view(), name='post_list'),

    # URL para detalhes de um post especifico (usando slug)
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
