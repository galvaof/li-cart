import pytest
from cart.usecases.retrieve_cart import RetrieveCart

class TestRetrieveCart:

    @pytest.fixture
    def usecase(self, non_empty_cart_repository):
        return RetrieveCart(non_empty_cart_repository)


    def test_when_cart_id_is_invalid_should_raise_error(self, usecase):
        with pytest.raises(RuntimeError):
            usecase.run(-1)

    def test_when_cart_id_is_valid_should_return_cart(self, usecase):
        response = usecase.run(1)
        assert response.id == 1