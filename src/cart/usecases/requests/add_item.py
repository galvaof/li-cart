class AddItemRequest:
    product_id: int
    quantity: int


class AddItemRequestBuilder:
    product_id = 1
    quantity = 1

    @staticmethod
    def a_request():
        return AddItemRequestBuilder()

    def with_product(self, product_id):
        self.product_id = product_id
        return self

    def with_quantity(self, quantity):
        self.quantity = quantity
        return self

    def build(self):
        req = AddItemRequest()
        req.product_id = self.product_id,
        req.quantity = self.quantity
        return req
