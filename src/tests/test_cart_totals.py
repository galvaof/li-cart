import pytest
from cart.usecases.get_cart_totals import GetCartTotals

allowed_error = 0.001

class TestCartTotals:

    @pytest.fixture
    def usecase(self, non_empty_cart_repository):
        return GetCartTotals(non_empty_cart_repository)

    def test_when_cart_not_in_repo_should_throw(self, usecase):
        with pytest.raises(RuntimeError):
            usecase.run(-1)

    def test_when_cart_in_repo_should_return_totals(self, usecase):
        response = usecase.run(1)

        assert response.subtotal == 1.11
        assert  -allowed_error <= (response.total - 0.999) <= allowed_error 