# blog_project/urls.py

from django.contrib import admin 
from django.urls import path, include # Importe o include para incluir URLs de outros arquivos 

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('blog.urls'))
]
