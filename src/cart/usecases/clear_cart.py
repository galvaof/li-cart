import cart.usecases.clear_cart

class ClearCart:

    def __init__(self,repository):
        self.repository = repository

    def run(self, cart_id):
        cart = self.repository.get(cart_id)

        cart.clear_items()

        self.repository.add(cart)

        return cart
