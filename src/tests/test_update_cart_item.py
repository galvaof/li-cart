import pytest
from cart.usecases.requests.cart_request import CartRequest
from cart.usecases.update_cart_item import UpdateCartItem

class TestUpdateCartItem:

    @pytest.fixture
    def usecase(self, non_empty_cart_repository):
        return UpdateCartItem(non_empty_cart_repository)

    @pytest.fixture
    def invalid_cart_request(self):
        req = CartRequest()
        req.cart_id = -1
        return req

    @pytest.fixture
    def invalid_product_request(self):
        return self._valid_cart_request(-1)

    @pytest.fixture
    def valid_request(self):
        return self._valid_cart_request(1)

    def _valid_cart_request(self, product_id):
        req = CartRequest()
        req.cart_id = 1
        req.product_id = product_id
        req.quantity = 2
        return req

    def test_when_cart_not_in_repo_should_throw(self, usecase, invalid_cart_request):
        with pytest.raises(RuntimeError):
            response = usecase.run(invalid_cart_request)

    def test_when_product_not_in_cart_should_throw(self, usecase, invalid_product_request):
        with pytest.raises(RuntimeError):
            response = usecase.run(invalid_product_request)

    def test_when_product_in_cart_should_update(self, usecase, valid_request):
        response = usecase.run(valid_request)

        assert response.id == valid_request.cart_id
        assert len(response.items) == 1
        assert response.items[0].product_id == valid_request.product_id
        assert response.items[0].quantity == valid_request.quantity

        

