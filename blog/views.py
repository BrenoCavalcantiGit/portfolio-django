from django.http import HttpResponse
from django.views.generic import DetailView, ListView

from .models import Post


def home(request):
    return HttpResponse('Hello World')


class SidebarMixin:
    """Envia os posts recentes para o template da sidebar."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.filter(published=True)[:5]
        return context


class PostListView(SidebarMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published=True)


class PostDetailView(SidebarMixin, DetailView):
    model = Post
    template_name = 'blog/detalhe.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(published=True)
