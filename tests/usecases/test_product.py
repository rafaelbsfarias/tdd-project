from typing import List
from uuid import UUID

import pytest
from store.core.exceptions import NotFoundException
from store.schemas.product import ProductOut, ProductUpdateOut
from store.usecases.product import product_usecase


async def test_usecases_create_should_return_success(product_in, mongo_client):
    result = await product_usecase.create(body=product_in)
    # Verifica o retorno do método create
    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"
    # Verifica diretamente no banco de dados
    # await mongo_client.get_database()["products"].find_one({"id": str(product_in.id)})
    # assert db_result is not None
    # assert db_result["name"] == "Iphone 14 pro Max"


async def test_usecases_get_should_return_success(product_inserted):
    result = await product_usecase.get(id=product_inserted.id)

    assert isinstance(result, ProductOut)
    assert result.name == "Iphone 14 pro Max"


async def test_usecases_get_should_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.get(id=UUID("63f8a0cf-465d-444d-afa1-5de30922530a"))
    assert (
        err.value.message
        == "Product not found with filter: 63f8a0cf-465d-444d-afa1-5de30922530a"
    )


@pytest.mark.usefixtures("products_inserted")
async def test_usecases_query_should_return_success():
    result = await product_usecase.query()

    assert isinstance(result, List)
    assert len(result) > 1


async def test_usecases_update_should_return_success(product_up, product_inserted):
    product_up.price = "7500.0"
    result = await product_usecase.update(id=product_inserted.id, body=product_up)
    assert isinstance(result, ProductUpdateOut)


async def test_usecases_delete_should_return_success(product_inserted):
    result = await product_usecase.delete(id=product_inserted.id)
    assert result is True


async def test_usecases_delete_should_not_found():
    with pytest.raises(NotFoundException) as err:
        await product_usecase.delete(id=UUID("63f8a0cf-465d-444d-afa1-5de30922530a"))
    assert (
        err.value.message
        == "Product not found with filter: 63f8a0cf-465d-444d-afa1-5de30922530a"
    )
