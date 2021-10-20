from .requests.add_item import AddItemRequest
from cart.entities.shopping_cart import ShoppingCart, CartItem


class AddItemToCart:

    def __init__(self, repository):
        self.repository = repository

    def run(self, request: AddItemRequest):
        if not (hasattr(request, 'product_id') and hasattr(request, 'quantity')):
            raise RuntimeError("bad request")

        if not hasattr(request, 'cart_id'):
            cart = ShoppingCart()
            cart.id = self.repository.get_next_id()
        else:
            cart = self.repository.get(request.cart_id)

        if request.product_id not in map(lambda x: x.product_id, cart.items):
            item = CartItem()
            item.product_id = request.product_id
            item.quantity = request.quantity

        else:
            item = next(x for x in cart.items if x.product_id ==
                        request.product_id)
            cart.items.remove(item)
            item.quantity += request.quantity

        cart.items.append(item)
        self.repository.add(cart)

        return cart
