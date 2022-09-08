import pytest

@pytest.mark.django_db
def test_selection_create(client, get_token, user, ad):
    response = client.post(
        "/ads/selection/create/",
        {
            "name": "new test selection",
            "owner": user.id,
            "items": [ad.Id]
        },
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {get_token}")

    assert response.status_code == 201
    assert response.data == {'id': 1, 'name': 'new test selection', 'owner': user.id, 'items': [ad.Id]}