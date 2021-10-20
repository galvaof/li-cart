class CartItem:
    product_id: int
    quantity: int


class ShoppingCart:
    id: int
    items: [CartItem]

    def __init__(self):
        self.items = []
