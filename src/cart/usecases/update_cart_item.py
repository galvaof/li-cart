from .requests.cart_request import CartRequest

class UpdateCartItem:
    def __init__(self, repository):
        self.repository = repository

    def run(self, request: CartRequest):
        cart = self.repository.get(request.cart_id)
        if not cart or not cart.has_item(request.product_id):
            raise RuntimeError

        item = cart.get_item(request.product_id)
        cart.remove(item)

        item.quantity = request.quantity
        cart.add(item)

        self.repository.add(cart)
        return cart
