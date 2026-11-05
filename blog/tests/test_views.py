from django.urls import reverse


def test_home_returns_hello_world(client):
    response = client.get('/home/')

    assert response.status_code == 200
    assert 'Hello World' in response.content.decode()


def test_home_url_name_points_to_home_path():
    assert reverse('home') == '/home/'


def test_home_without_trailing_slash_redirects(client):
    response = client.get('/home')

    assert response.status_code == 301
    assert response['Location'] == '/home/'


def test_unknown_route_returns_404(client):
    response = client.get('/rota-que-nao-existe/')

    assert response.status_code == 404
