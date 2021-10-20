class RemoveFromCart:

    def __init__(self, repository):
        self.repository = repository

    def run(self, cart_id, product_id):
        cart = self.repository.get(cart_id)
        if not cart:
            raise RuntimeError
        
        item = cart.get_item(product_id)
        cart.remove(item)
        self.repository.add(cart)
        
        return cart
