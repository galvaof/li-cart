class RetrieveCart:
    def __init__(self, repository):
        self.repository = repository

    def run(self, cart_id):
        cart = self.repository.get(cart_id)
        if not cart:
            raise RuntimeError("cart_id not found")
        return cart