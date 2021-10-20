from fastapi import FastAPI, HTTPException
from fastapi import  HTTPException
from cart.usecases.retrieve_cart import RetrieveCart
from fastapi.params import Depends
from fastapi import APIRouter
from functools import lru_cache
from cart.repositories.cart_repo import CartRepository
from cart.web.responses import CartItemDetailsSchema, CartTotalsSchema, CartItemDetailsSchema, ShoppingCartSchema,ShoppingCartDetailsSchema 
from cart.web.requests import CartItemRequest, RemoveItemRequest, VoucherRequest
from cart.usecases.requests.cart_request import CartRequestBuilder
from cart.usecases.add_to_cart import AddItemToCart
from cart.usecases.update_cart_item import UpdateCartItem
from cart.usecases.remove_from_cart import RemoveFromCart
from cart.usecases.clear_cart import ClearCart
from cart.usecases.apply_voucher import ApplyVoucher
from cart.usecases.get_cart_totals import GetCartTotals
from cart.services.catalog_service import CatalogService


router = APIRouter(prefix="/api/cart", tags=["cart"], )

repo = CartRepository()

@lru_cache
def get_repo() -> CartRepository:
    return repo

@router.post("/", status_code=201)
async def create_cart(payload: CartItemRequest, repo = Depends(get_repo)) -> ShoppingCartSchema:
    usecase = AddItemToCart(repo)
    req = CartRequestBuilder.a_request().with_product(payload.product_id).with_quantity(payload.quantity).build()
    try: 
        dto = usecase.run(req)
        return {
            "id": dto.id,
            "items": list(dto.items),
            "voucher": dto.voucher,
            "discount": dto.discount_ratio,
        }
    except:
        raise HTTPException(status_code=304, detail="Not enough inventory")


@router.post("/{id}/", status_code=202)
async def add_to_cart(id: int, payload: CartItemRequest, repo = Depends(get_repo)) -> ShoppingCartSchema:
    usecase = AddItemToCart(repo)
    req = CartRequestBuilder.a_request().oncart(id).with_product(payload.product_id).with_quantity(payload.quantity).build()
    try: 
        dto = usecase.run(req)
        return {
            "id": dto.id,
            "items": list(dto.items),
            "voucher": dto.voucher,
            "discount": dto.discount_ratio,
        }
    except:
        raise HTTPException(status_code=304, detail="Not enough inventory")

@router.patch("/{id}/", status_code=202)
async def update_cart(id: int, payload: CartItemRequest, repo = Depends(get_repo)) -> ShoppingCartSchema:
    usecase = UpdateCartItem(repo)
    req = CartRequestBuilder.a_request().oncart(id).with_product(payload.product_id).with_quantity(payload.quantity).build()
    try:
        dto = usecase.run(req)
        return {
        "id": dto.id,
        "items": list(dto.items),
        "voucher": dto.voucher,
        "discount": dto.discount_ratio,
    }
    except:
        raise HTTPException(status_code=304, detail="Not enough inventory")
    

@router.delete("/{id}/", status_code=202)
async def delete_from_cart(id: int, payload: RemoveItemRequest, repo = Depends(get_repo)) -> ShoppingCartSchema:
    usecase = RemoveFromCart(repo)
    dto = usecase.run(id,payload.product_id)
    return {
        "id": dto.id,
        "items": list(dto.items),
        "voucher": dto.voucher,
        "discount": dto.discount_ratio,
    }

@router.delete("/{id}/all", status_code=202)
async def clear_cart(id: int, repo = Depends(get_repo)) -> ShoppingCartSchema:
    usecase = ClearCart(repo)
    dto = usecase.run(id)
    return {
        "id": dto.id,
        "items": list(dto.items),
        "voucher": dto.voucher,
        "discount": dto.discount_ratio,
    }

@router.get("/{id}/")
async def retrieve_cart(id: int, repo = Depends(get_repo)) -> ShoppingCartSchema:
    usecase = RetrieveCart(repo)
    dto = usecase.run(id)
    return {
        "id": dto.id,
        "items": list(dto.items),
        "voucher": dto.voucher,
        "discount": dto.discount_ratio,
    }

@router.post("/{id}/voucher", status_code=202)
async def apply_voucher(id: int, payload: VoucherRequest, repo = Depends(get_repo)) -> ShoppingCartSchema:
    usecase = ApplyVoucher(repo)
    dto = usecase.run(id, payload.voucher)
    return {
        "id": dto.id,
        "items": list(dto.items),
        "voucher": dto.voucher,
        "discount": dto.discount_ratio,
    }

@router.get("/{id}/totals", status_code=200)
async def get_cart_totals(id: int, repo = Depends(get_repo)) -> CartTotalsSchema:
    usecase = GetCartTotals(repo)
    dto = usecase.run(id)
    return {
        "subtotal": float(format(dto.subtotal, '.2f')),
        "total": float(format(dto.total, '.2f')),
    }

@router.get("/{id}/details", status_code=200)
async def get_cart_totals(id: int, repo = Depends(get_repo)) -> ShoppingCartDetailsSchema:
    catalog = CatalogService()

    dto = RetrieveCart(repo).run(id)
    res = {
        "id": dto.id,
        "voucher": dto.voucher,
        "discount": dto.discount_ratio,
    }
    
    totals = GetCartTotals(repo).run(id)
    res["subtotal"] = float(format(totals.subtotal, '.2f'))
    res["total"] = float(format(totals.total, '.2f'))
    
    res["items"] = [CartItemDetailsSchema(
        product_id=item[0].product_id,
         quantity=item[0].quantity,
          name=item[1].name,
           price=float(format(item[1].price, '.2f')))
            for item in 
            [(item, catalog.get_product_info(item.product_id)) for item in dto.items]]
    return res
