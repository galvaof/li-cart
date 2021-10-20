class CartRequest:
    cart_id: int
    product_id: int
    quantity: int


class CartRequestBuilder:
    product_id:int = 1
    quantity:int = 1
    cart_id:int

    @staticmethod
    def a_request():
        return CartRequestBuilder()

    def __init__(self):
        self.cart_id = None

    def oncart(self, cart_id: int):
        self.cart_id = cart_id
        return self

    def with_product(self, product_id: int):
        self.product_id = product_id
        return self

    def with_quantity(self, quantity: int):
        self.quantity = quantity
        return self

    def build(self):
        req = CartRequest()
        req.product_id = self.product_id
        req.quantity = self.quantity
        if self.cart_id is not None:
            req.cart_id = self.cart_id
        return req
