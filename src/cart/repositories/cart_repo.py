class CartRepository:
    def __init__(self):
        self.data = {}
        self.next_id = 0

    def get_next_id(self):
        self.next_id += 1
        return self.next_id

    def get(self, id):
        if id not in self.data.keys():
            raise RuntimeError
        return self.data.get(id)

    def add(self, cart):
        self.data[cart.id] = cart
