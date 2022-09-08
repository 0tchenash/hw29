import pytest


@pytest.fixture
@pytest.mark.django_db
def get_token(client, django_user_model):
    username = "otche2"
    password = "123qwe"

    django_user_model.objects.create_user(username=username, password=password, role="admin")

    response = client.post("/user/token/", {'username': username, 'password': password}, format='json')
    return response.data["access"]