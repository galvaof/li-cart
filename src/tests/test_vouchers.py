import pytest
from cart.usecases.apply_voucher import ApplyVoucher

class TestVouchers:

    @pytest.fixture
    def usecase(self, non_empty_cart_repository):
        return ApplyVoucher(non_empty_cart_repository)

    def test_when_adding_bad_voucher_should_raise(self, usecase):
        with pytest.raises(RuntimeError):
            usecase.run(-1, "10OFF")

        with pytest.raises(RuntimeError):
            usecase.run(1, "bad_voucher")

    def test_when_adding_voucher_should_get_discount(self, usecase):
        response = usecase.run(1, "10OFF")

        assert response.voucher == "10OFF"
        assert response.discount_ratio == 0.1