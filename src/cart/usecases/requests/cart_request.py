class CartRequest:
    cart_id: int
    product_id: int
    quantity: int


class CartRequestBuilder:
    product_id = 1
    quantity = 1

    @staticmethod
    def a_request():
        return CartRequestBuilder()

    def with_product(self, product_id):
        self.product_id = product_id
        return self

    def with_quantity(self, quantity):
        self.quantity = quantity
        return self

    def build(self):
        req = CartRequest()
        req.product_id = self.product_id,
        req.quantity = self.quantity
        return req
