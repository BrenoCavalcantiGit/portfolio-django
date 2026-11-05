import pytest
from django.urls import reverse

from blog.tests.factories import PostFactory

pytestmark = pytest.mark.django_db


def test_index_uses_base_index_and_sidebar_templates(client):
    response = client.get(reverse('index'))

    names = [template.name for template in response.templates]
    assert response.status_code == 200
    assert 'blog/index.html' in names
    assert 'blog/base.html' in names
    assert 'blog/sidebar.html' in names


def test_index_lists_only_published_posts(client):
    PostFactory(title='Post publicado', published=True)
    PostFactory(title='Post rascunho', published=False)

    content = client.get(reverse('index')).content.decode()

    assert 'Post publicado' in content
    assert 'Post rascunho' not in content


def test_index_without_posts_shows_message(client):
    content = client.get(reverse('index')).content.decode()

    assert 'Nenhum post publicado ainda.' in content


def test_post_card_links_to_detail_page(client):
    post = PostFactory(published=True)

    content = client.get(reverse('index')).content.decode()

    assert reverse('post_detail', args=[post.pk]) in content


def test_detail_shows_full_post(client):
    post = PostFactory(
        title='Titulo completo',
        content='Conteudo completo do post',
        published=True,
    )

    response = client.get(reverse('post_detail', args=[post.pk]))

    content = response.content.decode()
    names = [template.name for template in response.templates]
    assert response.status_code == 200
    assert 'blog/detalhe.html' in names
    assert 'Titulo completo' in content
    assert 'Conteudo completo do post' in content


def test_detail_of_unpublished_post_returns_404(client):
    post = PostFactory(published=False)

    response = client.get(reverse('post_detail', args=[post.pk]))

    assert response.status_code == 404


def test_sidebar_lists_recent_posts_on_detail_page(client):
    first = PostFactory(title='Primeiro post', published=True)
    PostFactory(title='Segundo post', published=True)

    content = client.get(reverse('post_detail', args=[first.pk])).content.decode()

    assert 'Segundo post' in content
