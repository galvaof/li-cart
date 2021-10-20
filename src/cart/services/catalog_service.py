class CatalogProduct:
    price: float
    name: str

class CatalogService:

    def get_product_info(self, product_id):
        product = CatalogProduct()
        product.name = f"Product {product_id}"
        product.price = 1.11 * product_id
        
        return product