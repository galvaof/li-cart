class VoucherService:
    def get_discount(self, voucher):
        if voucher is "10OFF":
            return 0.1

        if voucher is "20OFF":    
            return 0.2

        raise RuntimeError("voucher not found")