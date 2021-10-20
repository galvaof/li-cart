from cart.services.inventory_services import InventoryService


class CartItem:
    product_id: int
    quantity: int


class ShoppingCart:
    id: int

    @property
    def items(self):
        return tuple(self._items)

    def __init__(self):
        self._items = []
        self.inventory = InventoryService()

    def get_item(self, product_id):
        if not self.has_item(product_id):
            raise RuntimeError
    
        return next(x for x in self.items if x.product_id ==
                        product_id)

    def has_item(self, product_id):
        return product_id in map(lambda x: x.product_id, self.items)

    def add(self, item: CartItem):
        if self.inventory.remaining(item.product_id) < item.quantity:
            raise RuntimeError("Not enough inventory")
        
        self._items.append(item)

    def remove(self, item):
        self._items.remove(item)
        
    def clear_items(self):
        self._items.clear()