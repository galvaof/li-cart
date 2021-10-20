import pytest
from cart.usecases.clear_cart import ClearCart

class TestClearCart:

    @pytest.fixture
    def usecase(self, non_empty_cart_repository):
        return ClearCart(non_empty_cart_repository)

    def test_when_cart_not_in_repo_should_throw(self, usecase):
        with pytest.raises(RuntimeError):
            usecase.run(-1)

    def test_when_cart_in_repo_should_clear_items(self, usecase):
        response = usecase.run(1)

        assert response.id == 1
        assert len(response.items) == 0