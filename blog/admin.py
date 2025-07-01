# blog/admin.py

from django.contrib import admin
from .models import Category, Post, Comment # Importe seus modelos

# Personalize a exibição de Post no Admin
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish_date', 'status')
    list_filter = ('status', 'created_at', 'publish_date', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)} # Preenche slug automaticamente a partir do título
    raw_id_fields = ('author',) # Para selecionar autor por ID em vez de dropdown
    date_hierarchy = 'publish_date' # Navegação por hierarquia de datas
    ordering = ('status', 'publish_date')

# Personalize a exibição de Comment no Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments', 'disapprove_comments'] # Ações personalizadas

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Aprovar comentários selecionados"

    def disapprove_comments(self, request, queryset):
        queryset.update(active=False)
    disapprove_comments.short_description = "Desaprovar comentários selecionados"

# Registre Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)