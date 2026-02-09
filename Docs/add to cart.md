
# PART 1 – What this document is (for your developer)

This document is for a **Web developer**

Goal of the document:

> After a negotiation is accepted by AI,
> automatically add the product to cart
> with final agreed price and quantity.

should:

* Not break existing APIs
* Not touch chat system
* Only extend system safely

---

# PART 2 – System Architecture (Explained Like 10 Year Old)

system has **3 parts**:

### 1. Laravel Website

This is the real user website:

* Users see products
* Users see cart
* Users checkout

### 2. AI Negotiation System (FastAPI on Render)

This is your AI brain:

* Talks to customer
* Negotiates price
* Decides final deal

### 3. Bridge API (Already Exists)

This connects both:

* Sends product + customer to AI
* Sends AI messages back to website

This bridge is **already working** and must NOT be touched.

---

# PART 3 – Where “Deal Accepted” Happens

In your AI system there is an endpoint:

```
POST /sessions/{session_id}/accept
```

This endpoint means:

> “Customer accepted the deal”

This is the **ONLY PLACE** we hook into.

We do NOT modify chat logic.
We only extend what happens after acceptance.

---

# PART 4 – Data We Need (Already Exists)

From your system, when a deal is accepted we already have:

From DB table `negotiation_sessions` (or similar):

* session_id
* product_id
* customer_id / mobile
* final_price
* final_quantity
* status = accepted

This is enough to add to cart.

No new AI logic needed.

---

# PART 5 – New Feature Design (Very Important)

We will build a **new mini layer**:

```
Deal Accepted
      |
      v
Cart Integration Service
      |
      v
Laravel Cart API
      |
      v
cart_items table
```

So flow becomes:

1. AI marks session accepted
2. AI calls Laravel: “add to cart”
3. Laravel inserts into cart table
4. User refreshes cart → sees product

---

# PART 6 – EXACT IMPLEMENTATION PLAN (Developer Guide)

This is what your new developer will follow.

---

## STEP 1 – Do NOT Touch Existing Chat Code

Rule for developer:

> You are not allowed to modify:
>
> * Chat APIs
> * Negotiation message logic
> * Existing controllers

Only add new code.

---

## STEP 2 – Create Cart Integration Service (AI Side)

File to create:

```
app/services/cart_integration.py
```

Paste this:

```python
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
```

---

## STEP 3 – Hook Into Deal Acceptance

File:

```
app/api/acceptance.py
```

Inside accept function:

```python
from app.services.cart_integration import add_to_cart_laravel

# after marking deal accepted
add_to_cart_laravel(
    product_id=session.product_id,
    quantity=session.final_quantity,
    price=session.final_price,
    customer_mobile=session.customer_mobile
)
```

That’s it on AI side.

No other change.

---

# PART 7 – Laravel Side (Cart API)

This is for Laravel developer.

## STEP 4 – Create New API Route

File:

```
routes/api.php
```

Add:

```php
Route::post('/cart/from-negotiation', [CartController::class, 'addFromNegotiation']);
```

---

## STEP 5 – Cart Controller

File:

```
app/Http/Controllers/CartController.php
```

Add:

```php
public function addFromNegotiation(Request $request)
{
    $productId = $request->product_id;
    $qty = $request->quantity;
    $price = $request->price;
    $mobile = $request->mobile;

    $customer = Customer::where('mobile', $mobile)->first();

    CartItem::create([
        'customer_id' => $customer->id,
        'product_id' => $productId,
        'quantity' => $qty,
        'price' => $price
    ]);

    return response()->json([
        'status' => 'success',
        'message' => 'Added to cart from negotiation'
    ]);
}
```

---

# PART 8 – Database (No Change Needed)

Uses existing table:

```
cart_items
```

Fields:

* customer_id
* product_id
* quantity
* price

---

# PART 9 – Testing Guide

This is the most important part for developer.

### Test Flow:

1. Open website
2. Start negotiation
3. Chat with AI
4. Accept deal
5. Open DB → cart_items
6. Refresh cart page
7. Product must appear

---

## Manual API Test

From browser or Postman:

```
POST https://ai-system/sessions/{id}/accept
```

Then:

```
SELECT * FROM cart_items ORDER BY id DESC;
```

If record exists → system works.

---

# PART 10 – Golden Rules for You

These are non-negotiable:

### Rule 1

Auto-cart must NEVER modify chat logic.

### Rule 2

Auto-cart must be its own service.

### Rule 3

If cart fails, negotiation still works.

### Rule 4

Never deploy this on production first.
Always use staging Render.

---


