Final Architecture (what we are building)
Browser (User)
   ↓
Laravel (PHP)
   ↓ HTTP
FastAPI (Render)
   ↓
DB + Negotiation Brain + LLM

Laravel never thinks. It only: collects data | sends to FastAPI | shows response

----------------------------------------------------------------------------------------------------------------------------------
Step C1 – We define the 2 endpoints in Laravel

Laravel only needs to know these:

POST https://ai-negotiation-staging.onrender.com/web/session/start
POST https://ai-negotiation-staging.onrender.com/messages/

Nothing else.
----------------------------------------------------------------------------------------------------------------------------------
Step C2 – Create Laravel controller

Tell your Laravel dev (or you do):

Create file:

app/Http/Controllers/AiNegotiationController.php  __ This is your entire integration layer.
----------------------------------------------------------------------------------------------------------------------------------
Step C3 – Define routes

In: routes/web.php

Add:

use App\Http\Controllers\AiNegotiationController;

Route::post("/ai/start-session", [AiNegotiationController::class, "startSession"]);
Route::post("/ai/send-message", [AiNegotiationController::class, "sendMessage"]);
---------------------------------------------------------------------------------------------------------------------------------
What Step C4 actually means (in simple words)

Step C4 = “How the user’s browser talks to Laravel.”

So far we did:

FastAPI → ready

Laravel → ready (controller + routes)

Now we connect:

User screen (HTML) → Laravel → AI system

---

# The simplest possible real implementation

We will make a **single test page** first.
Not full design. Just proof that integration works.

----------------

## Step 1 — Create a test page in Laravel

Create file: resources/views/ai_test.blade.php

Put this exact code:

```html
<!DOCTYPE html>
<html>
<head>
    <title>AI Negotiation Test</title>
</head>
<body>

<h2>Start Session</h2>
<input id="name" placeholder="Name" value="Akash">
<input id="phone" placeholder="Phone" value="9999999999">
<input id="product" placeholder="Product ID">
<button onclick="startSession()">Start</button>

<h2>Chat</h2>
<input id="message" placeholder="Your message">
<button onclick="sendMessage()">Send</button>

<pre id="chat"></pre>

<script>
let sessionId = null;

function startSession() {
    fetch("/ai/start-session", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: document.getElementById("name").value,
            phone_number: document.getElementById("phone").value,
            product_id: document.getElementById("product").value
        })
    })
    .then(res => res.json())
    .then(data => {
        sessionId = data.session_id;
        document.getElementById("chat").innerText += "Session started: " + sessionId + "\n";
    });
}

function sendMessage() {
    fetch("/ai/send-message", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            session_id: sessionId,
            message: document.getElementById("message").value
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("chat").innerText += "AI: " + data.message + "\n";
    });
}
</script>

</body>
</html>
```

---

## Step 2 — Add route to open this page

In: routes/web.php

Add:
php
Route::get("/ai-test", function () {
    return view("ai_test");
});

---

## Step 3 — Open in browser

Run Laravel:

```bash
php artisan serve
```

Open:

```
http://127.0.0.1:8000/ai-test
```

---

# This page is your integration laboratory

On this page you:

1. Paste real `product_id`
2. Click **Start**
3. Type message
4. Click **Send**
5. See AI reply

If this works:

> Your entire website integration is **100% solved**

Everything else is just UI design.

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Real production flow (no inputs)

In real UI, there will be ZERO input fields.

The JS will look like:

fetch("/ai/start-session", {
  method: "POST",
  headers: {"Content-Type": "application/json"},
  body: JSON.stringify({
    name: "{{ auth()->user()->name }}",
    phone_number: "{{ auth()->user()->phone_number }}",
    product_id: "{{ $product->uuid }}"
  })
});


User never sees this.

So where do values really come from?
Data	Comes from
name	Laravel auth user
phone	Laravel auth user
product_id	Product page context
language	hardcoded or user setting
