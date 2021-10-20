class RetrieveCart:
    def __init__(self, repository):
        self.repository = repository

    def run(self, cart_id):
        cart = self.repository.get(cart_id)
        return cart