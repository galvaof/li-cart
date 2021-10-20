import pytest
from cart.repositories.cart_repo import CartRepository
from cart.usecases.retrieve_cart import RetrieveCart
from cart.entities.shopping_cart import ShoppingCart

class TestRetrieveCart:

    @pytest.fixture
    def repository(self):
        repo = CartRepository()

        one_cart = ShoppingCart()
        one_cart.id = 1
        repo.add(one_cart)

        return repo

    @pytest.fixture
    def usecase(self, repository):
        return RetrieveCart(repository)


    def test_when_cart_id_is_invalid_should_raise_error(self, usecase):
        with pytest.raises(RuntimeError):
            usecase.run(-1)

    def test_when_cart_id_is_valid_should_return_cart(self, usecase):
        response = usecase.run(1)
        assert response.id == 1