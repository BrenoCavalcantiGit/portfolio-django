import pytest
from django.urls import reverse

from blog.models import Post
from blog.tests.factories import PostFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_post_is_registered_in_admin(admin_client):
    response = admin_client.get(reverse('admin:blog_post_changelist'))

    assert response.status_code == 200


def test_admin_lists_post_titles(admin_client):
    PostFactory(title='Post no admin')

    response = admin_client.get(reverse('admin:blog_post_changelist'))

    assert 'Post no admin' in response.content.decode()


def test_post_can_be_created_in_admin(admin_client):
    author = UserFactory()

    response = admin_client.post(
        reverse('admin:blog_post_add'),
        {
            'author': author.pk,
            'title': 'Criado pelo admin',
            'content': 'Conteudo do post',
        },
    )

    assert response.status_code == 302
    assert Post.objects.filter(title='Criado pelo admin').exists()


def test_publish_action_marks_posts_as_published(admin_client):
    posts = PostFactory.create_batch(2)

    response = admin_client.post(
        reverse('admin:blog_post_changelist'),
        {
            'action': 'publish_posts',
            'index': 0,
            '_selected_action': [post.pk for post in posts],
        },
    )

    assert response.status_code == 302
    assert Post.objects.filter(published=True).count() == 2


def test_unpublish_action_marks_posts_as_not_published(admin_client):
    posts = PostFactory.create_batch(2, published=True)

    response = admin_client.post(
        reverse('admin:blog_post_changelist'),
        {
            'action': 'unpublish_posts',
            'index': 0,
            '_selected_action': [post.pk for post in posts],
        },
    )

    assert response.status_code == 302
    assert Post.objects.filter(published=True).count() == 0
