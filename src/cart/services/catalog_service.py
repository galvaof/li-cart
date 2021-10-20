class CatalogService:

    def get_product_info(self, product_id):
        prod = object()

        prod.name = f"Product {product_id}"
        prod.price = 1.11 * product_id