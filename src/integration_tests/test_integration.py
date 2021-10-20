import json

import pytest

BASE_URL = "/api/cart"
ALLOWED_ERROR = 0.001

def test_create_a_cart(test_app):
    response = test_app.post(
        f"{BASE_URL}/", 
        data=json.dumps(
            {
                "product_id": "1",
                "quantity": "1",
            }
        )
    )
    response_data = response.json()

    assert_status_code(response, 201)
    assert response_data["id"] == 1
    assert len(response_data["items"]) == 1
    assert response_data["items"][0]["product_id"] == 1
    assert response_data["items"][0]["quantity"] == 1

def test_retrieve_cart(test_app):
    response = test_app.get(f"{BASE_URL}/1/")
    response_data = response.json()

    assert_status_code(response, 200)
    assert response_data["id"] == 1
    assert len(response_data["items"]) == 1
    assert response_data["items"][0]["product_id"] == 1
    assert response_data["items"][0]["quantity"] == 1

def assert_status_code(response, code):
    assert response.status_code == code



def test_add_to_existing_cart(test_app):
    response = add_to_cart(test_app, product=2, quantity=2)
    response_data = response.json()

    assert_status_code(response, 202)
    assert response_data["id"] == 1
    assert len(response_data["items"]) == 2
    assert response_data["items"][1]["product_id"] == 2
    assert response_data["items"][1]["quantity"] == 2

def test_voucher(test_app):
    response = test_app.post(
        f"{BASE_URL}/1/voucher", 
        data=json.dumps(
                {
                    "voucher": "10OFF"
                }
            ))
    response_data = response.json()

    assert_status_code(response, 202)
    assert response_data["id"] == 1
    assert len(response_data["items"]) == 2
    assert response_data["voucher"] == "10OFF"
    assert response_data["discount"] == 0.1

def test_totals(test_app):
    response = test_app.get(f"{BASE_URL}/1/totals")
    response_data = response.json()
    
    assert_status_code(response, 200)
    assert response_data["subtotal"] == 5.55
    assert response_data["total"] == 5.00

def test_cart_details(test_app):
    response = test_app.get(f"{BASE_URL}/1/details")
    response_data = response.json()
    
    assert_status_code(response, 200)
    assert response_data["id"] == 1
    assert len(response_data["items"]) == 2
    assert response_data["voucher"] == "10OFF"
    assert response_data["discount"] == 0.1
    assert response_data["subtotal"] == 5.55
    assert response_data["total"] == 5.00

def test_update_cart(test_app):
    response = test_app.patch(
        f"{BASE_URL}/1/", 
        data=json.dumps(
                {
                    "product_id": "1",
                    "quantity": "3",
                }
            ))
    response_data = response.json()

    assert_status_code(response, 202)
    assert response_data["id"] == 1
    assert len(response_data["items"]) == 2
    assert response_data["items"][1]["product_id"] == 1
    assert response_data["items"][1]["quantity"] == 3

def test_remove_item_from_cart(test_app):
    response = test_app.delete(
        f"{BASE_URL}/1/", 
        data=json.dumps(
                {
                    "product_id": "2"
                }
            ))
    response_data = response.json()

    assert_status_code(response, 202)
    assert response_data["id"] == 1
    assert len(response_data["items"]) == 1
    assert response_data["items"][0]["product_id"] == 1
    assert response_data["items"][0]["quantity"] == 3

def test_clear_cart(test_app):
    response = test_app.delete(f"{BASE_URL}/1/all")
    response_data = response.json()

    assert_status_code(response, 202)
    assert response_data["id"] == 1
    assert len(response_data["items"]) == 0

def test_add_more_than_in_inventory(test_app):
    response = add_to_cart(test_app, quantity=10)
    response_data = response.json()

    assert_status_code(response, 304)

def add_to_cart(test_app, cart_id=1, product=1, quantity=1):
    return test_app.post(
        f"{BASE_URL}/{cart_id}/", 
        data=json.dumps(
            {
                "product_id": product,
                "quantity": quantity,
            }
        )
    )