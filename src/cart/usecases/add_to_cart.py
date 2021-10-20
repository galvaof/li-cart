from .requests.cart_request import CartRequest
from cart.entities.shopping_cart import ShoppingCart, CartItem


class AddItemToCart:

    def __init__(self, repository):
        self.repository = repository
        

    def run(self, request: CartRequest):
        if not (hasattr(request, 'product_id') and hasattr(request, 'quantity')):
            raise RuntimeError("bad request")

        if not hasattr(request, 'cart_id'):
            cart = ShoppingCart()
            cart.id = self.repository.get_next_id()
        else:
            cart = self.repository.get(request.cart_id)

        if not cart.has_item(request.product_id):
            item = CartItem()
            item.product_id = request.product_id
            item.quantity = request.quantity
        else:
            item = cart.get_item(request.product_id)
            cart.remove(item)
            item.quantity += request.quantity

        
        
        cart.add(item)
        self.repository.add(cart)

        return cart
