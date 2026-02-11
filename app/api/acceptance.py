from app.services.cart_integration import add_to_cart_laravel

# after marking deal accepted
add_to_cart_laravel(
    product_id=session.product_id,
    quantity=session.final_quantity,
    price=session.final_price,
    customer_mobile=session.customer_mobile
)