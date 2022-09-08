import pytest

from ads.serializers import AdDetailSerializer


@pytest.mark.django_db
def test_ads_create(client, ad, get_token):
    response = client.get(
        f"/ads/{ad.Id}/",
        content_type="application/json",
        HTTP_AUTHORIZATION=f"Bearer {get_token}")

    assert response.status_code == 200
    assert response.data == AdDetailSerializer(ad).data