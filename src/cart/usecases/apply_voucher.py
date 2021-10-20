from cart.services.voucher_service import VoucherService


class ApplyVoucher:
    def __init__(self, repository):
        self.repository = repository
        self.vouchers = VoucherService()
        

    def run(self, cart_id, voucher):
        cart = self.repository.get(cart_id)
        
        cart.discount_ratio = self.vouchers.get_discount(voucher)
        cart.voucher = voucher
        
        self.repository.add(cart)
        return cart
