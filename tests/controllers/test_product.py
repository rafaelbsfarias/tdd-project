from typing import List

from httpx import AsyncClient
import pytest
from tests.factories import product_data
from fastapi import status


async def test_controller_create_should_return_success(client, products_url):
    response = await client.post(products_url, json=product_data())

    content = response.json()
    del content["created_at"]
    del content["updated_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


async def test_controller_get_should_return_success(
    client, products_url, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()
    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


async def test_controller_get_should_not_found(client, products_url):
    response = await client.get(f"{products_url}f6cb1ec6-d486-40e9-b5c2-302d7fbc729e")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: f6cb1ec6-d486-40e9-b5c2-302d7fbc729e"
    }


@pytest.mark.usefixtures("products_inserted")
async def test_controller_query_should_return_success(client, products_url):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_delete_should_return_no_content(
    client, products_url, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_should_not_found(client, products_url):
    response = await client.delete(
        f"{products_url}f6cb1ec6-d486-40e9-b5c2-302d7fbc729e"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: f6cb1ec6-d486-40e9-b5c2-302d7fbc729e"
    }


async def test_controller_patch_should_return_success(
    client, products_url, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )

    content = response.json()

    del content["created_at"]
    del content["updated_at"]

    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "id": str(product_inserted.id),
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "7.500",
        "status": True,
    }


@pytest.mark.asyncio
async def test_controller_patch_should_return_fail(
    client: AsyncClient, product_inserted
):
    product_id = product_inserted.id

    # Captura o created_at ANTES da atualização
    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 200
    product_before = response.json()
    created_at_before = product_before["created_at"]

    # Atualiza o produto
    update_payload = {"quantity": 10, "price": 35000, "status": True}
    response = await client.patch(f"/products/{product_id}", json=update_payload)
    assert response.status_code == 200

    # Captura o created_at DEPOIS da atualização
    product_after = response.json()
    created_at_after = product_after["created_at"]

    # Se o created_at mudou, isso indica um problema, então o teste deve falhar intencionalmente
    assert (
        created_at_before != created_at_after
    ), "O campo created_at deveria permanecer inalterado, mas foi modificado"
