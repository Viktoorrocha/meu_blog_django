# blog/tests.py

from django.test import TestCase # Importa a classe base de testes do Django
from django.contrib.auth import get_user_model # Para obter o modelo de usuário do Django
from django.utils import timezone
from .models import Category, Post, Comment # Importa seus modelos

# Obtém o modelo de usuário padrão do Django
User = get_user_model()

class CategoryModelTest(TestCase):
    """
    Testes para o modelo Category.
    """
    def setUp(self):
        # Configura um objeto Category que será usado em vários testes
        self.category = Category.objects.create(name='Technology')

    def test_category_creation(self):
        """Testa se uma categoria é criada corretamente."""
        self.assertTrue(isinstance(self.category, Category)) # Verifica se é uma instância de Category
        self.assertEqual(self.category.__str__(), 'Technology') # Testa o método __str__
        self.assertEqual(Category.objects.count(), 1) # Verifica se há apenas 1 categoria no banco

    def test_unique_category_name(self):
        """Testa se nomes de categoria devem ser únicos."""
        with self.assertRaises(Exception): # Espera que uma exceção seja levantada
            Category.objects.create(name='Technology') # Tenta criar uma categoria com nome duplicado

class PostModelTest(TestCase):
    """
    Testes para o modelo Post.
    """
    def setUp(self):
        # Configura um usuário e uma categoria para os posts
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Science')
        # Cria um objeto Post para ser usado em vários testes
        self.post = Post.objects.create(
            title='My Test Post',
            slug='my-test-post',
            author=self.user,
            category=self.category,
            body='This is the body of my test post.',
            status='published'
        )

    def test_post_creation(self):
        """Testa se um post é criado corretamente."""
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.__str__(), 'My Test Post')
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
        self.assertEqual(self.post.status, 'published')
        self.assertIsNotNone(self.post.publish_date) # Verifica se a data de publicação foi definida

    def test_post_slug_uniqueness(self):
        """Testa se o slug do post é único."""
        with self.assertRaises(Exception):
            Post.objects.create(
                title='Another Test Post',
                slug='my-test-post', # Slug duplicado
                author=self.user,
                category=self.category,
                body='Another body.',
                status='draft'
            )

    def test_post_status_default(self):
        """Testa se o status padrão do post é 'draft'."""
        post_draft = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            author=self.user,
            body='This is a draft.'
        )
        self.assertEqual(post_draft.status, 'draft')

class CommentModelTest(TestCase):
    """
    Testes para o modelo Comment.
    """
    def setUp(self):
        # Configura um usuário, categoria e post para os comentários
        self.user = User.objects.create_user(username='commenteruser', password='password123')
        self.category = Category.objects.create(name='General')
        self.post = Post.objects.create(
            title='Post for Comments',
            slug='post-for-comments',
            author=self.user,
            category=self.category,
            body='This post will receive comments.',
            status='published'
        )
        # Cria um objeto Comment que será o mais antigo em termos de timestamp se usado em outros testes
        self.comment = Comment.objects.create(
            post=self.post,
            name='John Doe',
            email='john@example.com',
            body='This is a test comment from setUp.', # Opcional: mude o corpo para diferenciar melhor no debug
            active=True
        )

    def test_comment_creation(self):
        """Testa se um comentário é criado corretamente."""
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(self.comment.__str__(), f'Comment by John Doe on {self.post}')
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.post, self.post)
        self.assertTrue(self.comment.active) # Verifica se o comentário está ativo

    def test_comment_default_active_status(self):
        """Testa se o status padrão do comentário é ativo (True)."""
        comment_default = Comment.objects.create(
            post=self.post,
            name='Jane Doe',
            email='jane@example.com',
            body='Another test comment.'
        )
        self.assertTrue(comment_default.active) # Verifica se o padrão é True

    def test_comment_ordering(self):
        """Testa se os comentários são ordenados por data de criação."""
        # Criar alguns comentários com datas ligeiramente diferentes
        # Garanta que as datas sejam posteriores ao self.comment do setUp
        # Ou ajuste a expectativa para incluir self.comment no início.

        # Criar os comentários explicitamente com datas para garantir a ordem
        # As datas devem ser *depois* do created_at de self.comment
        # Usaremos seconds para garantir que as datas sejam distintas e em ordem.
        # O created_at de self.comment é definido quando setUp() é executado.
        base_time = self.comment.created_at # Pega o timestamp do comentário do setUp

        comment3 = Comment.objects.create(post=self.post, name='C', email='c@c.com', body='3', created_at=base_time + timezone.timedelta(seconds=1))
        comment1 = Comment.objects.create(post=self.post, name='A', email='a@a.com', body='1', created_at=base_time + timezone.timedelta(seconds=2))
        comment2 = Comment.objects.create(post=self.post, name='B', email='b@b.com', body='2', created_at=base_time + timezone.timedelta(seconds=3))


        # Recuperar todos os comentários e garantir que estão ordenados
        # A classe Meta do modelo Comment já define ordering = ['created_at']
        ordered_comments = Comment.objects.all()

        # A ordem esperada é: self.comment (o mais antigo), seguido por comment3, comment1, comment2
        self.assertEqual(list(ordered_comments), [self.comment, comment3, comment1, comment2])