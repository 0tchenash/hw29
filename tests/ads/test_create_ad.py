import pytest


@pytest.mark.django_db
def test_ads_create(client, user, category, get_token):
    response = client.post(
        "/ads/create/",
        {
            "name": "new test ad",
            "price": 10,
            "description": "test description",
            "is_published": False,
            "author": user.username,
            "category": category.id
        },
        content_type="application/json",
        HTTP_AUTHORIZATION = f"Bearer {get_token}")

    assert response.status_code == 201
    assert response.data == {
        'Id': 1,
        'author': user.username,
        'category': category.id,
        'description': 'test description',
        'is_published': False,
        'name': 'new test ad',
        'price': 10,
    }