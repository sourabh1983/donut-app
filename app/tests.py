from rest_framework.reverse import reverse
import pytest

from . import enums
from . import factories
from . import models


@pytest.mark.django_db()
def test_get_donuts(client):
    donut = factories.Donut()

    url = reverse("v1-donuts:list_create_donut")
    response = client.get(url).json()

    assert response == [
        {
            "id": str(donut.id),
            "code": donut.code,
            "description": donut.description,
            "price_per_unit": donut.price_per_unit,
        }
    ]


@pytest.mark.django_db()
def test_search_donut(client):
    donuts = [
        factories.Donut(description="Apple"),
        factories.Donut(description="Orange"),
    ]

    url = f'{reverse("v1-donuts:list_create_donut")}?q=oran'
    response = client.get(url).json()

    assert response == [
        {
            "id": str(donuts[1].id),
            "code": donuts[1].code,
            "description": donuts[1].description,
            "price_per_unit": donuts[1].price_per_unit,
        }
    ]


@pytest.mark.django_db()
def test_create_donut(client):
    assert models.Donut.objects.count() == 0

    url = reverse("v1-donuts:list_create_donut")
    response = client.post(
        url,
        data={"code": "XYZ", "price_per_unit": 10.0, "description": "X Donut"},
        format="json",
    )

    assert response.status_code == 201
    assert models.Donut.objects.count() == 1


@pytest.mark.django_db()
def test_get_donut_by_id(client):
    donut = factories.Donut()

    url = reverse("v1-donuts:retrieve_update_destroy_donut", kwargs={"pk": donut.id})
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == {
        "id": str(donut.id),
        "code": donut.code,
        "description": donut.description,
        "price_per_unit": donut.price_per_unit,
    }


@pytest.mark.django_db()
def test_update_donut_by_id(client):
    donut = factories.Donut(description="A Donut", code="ABC")

    url = reverse("v1-donuts:retrieve_update_destroy_donut", kwargs={"pk": donut.id})
    response = client.patch(
        path=url,
        data={"code": "XYZ", "price_per_unit": 10.0, "description": "X Donut"},
        content_type="application/json",
    )

    assert response.status_code == 200
    donut.refresh_from_db()
    assert donut.price_per_unit == 10.0
    assert donut.code == "XYZ"
    assert donut.description == "X Donut"


@pytest.mark.django_db()
def test_create_order(client):
    factories.Donut(code="A DONUT"),
    factories.Donut(code="B DONUT"),

    url = reverse("v1-donuts:create_order")
    payload = {
        "donuts": [
            {"donut_code": "A DONUT", "quantity": 3},
            {"donut_code": "B DONUT", "quantity": 1},
        ]
    }

    response = client.post(
        url,
        payload,
        content_type="application/json",
    )

    assert response.status_code == 201
    assert models.Order.objects.count() == 2


@pytest.mark.django_db()
def test_get_orders(client):
    donut = factories.Donut()
    order = factories.Order(donut_code=donut)

    url = reverse("v1-donuts:list_order")
    response = client.get(url).json()

    assert len(response) == 1
    assert response[0]["id"] == str(order.id)
    assert response[0]["donut_code"] == donut.code
    assert response[0]["state"] == enums.OrderStatus.CREATED.value
