import requests

def add_to_cart_laravel(product_id, quantity, price, customer_mobile):
    url = "https://YOUR-LARAVEL-SITE/api/cart/from-negotiation"
    
    payload = {
        "product_id": product_id,
        "quantity": quantity,
        "price": price,
        "mobile": customer_mobile
    }

    response = requests.post(url, json=payload, timeout=10)
    return response.json()