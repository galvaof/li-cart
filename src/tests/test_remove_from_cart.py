import pytest
from cart.usecases.remove_from_cart import RemoveFromCart


class TestRemoveFromCart:

    @pytest.fixture
    def usecase(self, non_empty_cart_repository):
        return RemoveFromCart(non_empty_cart_repository)

    def test_when_removing_non_added_product_should_raise_error(self, usecase):
        with pytest.raises(RuntimeError):
            usecase.run(1,2)

        with pytest.raises(RuntimeError):
            usecase.run(2,1)

    def test_when_removing_added_product_should_return_updated_cart(self, usecase):
        response = usecase.run(1, 1)
        assert response.id == 1
        assert len(response.items) == 0