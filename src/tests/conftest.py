import pytest
from cart.repositories.cart_repo import CartRepository
from cart.entities.shopping_cart import ShoppingCart, CartItem

@pytest.fixture
def cart_repository():
    return CartRepository()

@pytest.fixture
def non_empty_cart_repository(cart_repository):
    one_cart = ShoppingCart()
    one_cart.id = 1

    item = CartItem
    item.product_id = 1
    item.quantity = 1
    one_cart.add(item)

    cart_repository.add(one_cart)
    return cart_repository

