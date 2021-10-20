from cart.services.catalog_service import CatalogService

class CartTotals:
    total: float
    subtotal: float

class GetCartTotals:
    def __init__(self, repository):
        self.repository = repository
        self.catalog = CatalogService()
        

    def run(self, cart_id):
        cart = self.repository.get(cart_id)

        subtotal = 0

        for item in cart.items:
            info = self.catalog.get_product_info(item.product_id)
            subtotal += item.quantity * info.price
        
        total = (1-cart.discount_ratio) * subtotal

        dto = CartTotals()
        dto.subtotal = subtotal
        dto.total = total 

        return dto