import pytest
import copy
from collections import Counter
from cart.usecases.add_to_cart import AddItemToCart
from cart.usecases.requests.cart_request import CartRequest, CartRequestBuilder


def comparable_response(iterable):
    return Counter(map(lambda item: (item.product_id, item.quantity), iterable))


def contains_in_any_order(actual, expected):
    return comparable_response(actual) == comparable_response(expected)


class TestAddToCart:

    @pytest.fixture
    def usecase(self, cart_repository):
        return AddItemToCart(cart_repository)

    @pytest.fixture
    def empty_request(self):
        return CartRequest()

    @pytest.fixture
    def new_cart_request(self):
        return self.make_request(1)

    def make_request(self, product, quantity=1):
        return CartRequestBuilder.a_request().with_product(
            product).with_quantity(quantity).build()

    def test_when_empty_request_should_raise_error(self, usecase, empty_request):
        with pytest.raises(RuntimeError):
            usecase.run(empty_request)

        incomplete_request = copy.copy(empty_request)
        incomplete_request.quantity = 1
        with pytest.raises(RuntimeError):
            usecase.run(empty_request)

        incomplete_request = copy.copy(empty_request)
        incomplete_request.product_id = 1
        with pytest.raises(RuntimeError):
            usecase.run(empty_request)

    def test_when_first_run_should_create_cart(self, usecase, new_cart_request):
        response = usecase.run(new_cart_request)

        assert response.id
        assert len(response.items) == 1
        assert response.items[0].product_id == new_cart_request.product_id
        assert response.items[0].quantity == new_cart_request.quantity

    def test_when_run_second_time_should_create_second_cart(self, usecase, new_cart_request):
        first_response = usecase.run(new_cart_request)

        second_response = usecase.run(new_cart_request)

        assert second_response.id != first_response.id
        assert len(second_response.items) == 1
        assert contains_in_any_order(first_response.items, [new_cart_request])

    def test_when_run_twice_should_accumulate_quantities(self, usecase, new_cart_request):
        first_response = usecase.run(new_cart_request)

        new_cart_request.cart_id = first_response.id
        second_response = usecase.run(new_cart_request)

        # expected quantity should be double the original quantity
        new_cart_request.quantity *= 2

        assert second_response.id == first_response.id
        assert len(second_response.items) == 1
        assert contains_in_any_order(second_response.items, [new_cart_request])

    def test_when_run_with_two_items_should_accumulate_items(self, usecase, new_cart_request):
        first_response = usecase.run(new_cart_request)

        second_request = self.make_request(2)
        second_request.cart_id = first_response.id

        actual_response = usecase.run(second_request)

        assert actual_response.id == first_response.id
        assert len(actual_response.items) == 2
        assert contains_in_any_order(actual_response.items, [
                                     new_cart_request, second_request])


    def test_when_not_enough_inventory(self, usecase, new_cart_request):
        new_cart_request.quantity = 5
        with pytest.raises(RuntimeError):
            usecase.run(new_cart_request)