# blog/views.py 

from django.views.generic import ListView, DetailView 
from .models import Post, Category, Comment # importa os modelos 

class PostListView(ListView):
    model = Post # Indica qual modelo deve usar 
    template_name = 'blog/post_list.html' # Indica qual template usar
    context_object_name = 'posts' # Nome da variável que será passada para o template (por padrão seria 'object_list')
    queryset = Post.objects.filter(status='published').order_by('-publish_date') # Filtra apenas posts publicados
    paginate_by = 10 # Define a quantidade de posts por página


class PostDetailView(DetailView):
    model = Post # Indica qual modelo deve usar
    template_name = 'blog/post_detail.html' # Indica qual template usar 
    context_object_name = 'post' # Nome da variável que será passada para o template
    slug_field = 'slug' # Indica que a URL usa o campo slug para buscar o objeto
    slug_url_kwarg = 'slug' # Garante que o argumento da URL seja 'slug'


    def get_queryset(self):
        # Garante que apenas posts publicados serão mostrados
        return Post.objects.filter(status='published')
    
    def get_context_data(self, **kwargs):
        # Adiciona os comentários e o formulário de comentários ao contexto
        context = super().get_context_data(**kwargs)

        # Carrega apenas comentários ativos para este post 
        context['comments'] = self.object.comments.filter(active=True)
        # No momento não temos o formulário de comentários, mas vamos deixar pronto.
        # from .forms import CommentForm # Isso será descomentado na Tarefa 13
        # context['comment_form'] = CommentForm() # Isso será descomentado na Tarefa 13
        return context



