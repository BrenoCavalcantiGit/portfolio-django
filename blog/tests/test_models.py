import pytest

from blog.models import Post
from blog.tests.factories import PostFactory, UserFactory

pytestmark = pytest.mark.django_db


def test_post_str_returns_title():
    post = PostFactory(title='Meu primeiro post')

    assert str(post) == 'Meu primeiro post'


def test_post_is_saved_in_database():
    post = PostFactory()

    assert Post.objects.count() == 1
    assert Post.objects.filter(pk=post.pk).exists()


def test_post_is_not_published_by_default():
    post = PostFactory()

    assert post.published is False


def test_post_can_be_published():
    PostFactory(published=True)

    assert Post.objects.filter(published=True).count() == 1


def test_post_dates_are_filled_automatically():
    post = PostFactory()

    assert post.created_at is not None
    assert post.updated_at is not None


def test_updated_at_is_refreshed_when_post_is_saved_again():
    post = PostFactory()
    first_update = post.updated_at

    post.title = 'Novo titulo'
    post.save()
    post.refresh_from_db()

    assert post.updated_at >= first_update


def test_posts_are_ordered_from_newest_to_oldest():
    first = PostFactory()
    second = PostFactory()

    assert list(Post.objects.all()) == [second, first]


def test_post_belongs_to_author():
    user = UserFactory()
    post = PostFactory(author=user)

    assert post.author == user
    assert list(user.posts.all()) == [post]


def test_deleting_author_deletes_posts():
    post = PostFactory()

    post.author.delete()

    assert Post.objects.count() == 0
