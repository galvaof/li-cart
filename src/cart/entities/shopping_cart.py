class CartItem:
    product_id: int
    quantity: int


class ShoppingCart:
    id: int
    items: [CartItem]

    def __init__(self):
        self.items = []

    def get_item(self, product_id):
        if not self.has_item(product_id):
            raise RuntimeError
    
        return next(x for x in self.items if x.product_id ==
                        product_id)

    def has_item(self, product_id):
        return product_id in map(lambda x: x.product_id, self.items)