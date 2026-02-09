Below is the **complete handover implementation document**.

---

# Admin Product Excel Upload – Implementation Guid

**Project: AI Agro Negotiation System (FastAPI Backend)**

## 1. Purpose of This Document

This document explains how to implement an **admin-only feature** that allows uploading an **Excel or CSV file** to insert product data into the database.

This product data is used by the AI system to perform negotiations.
Without this data, the AI cannot function properly.

This is a **one-time / rare admin operation**, not for customers.

---

## 2. What This Feature Does (In Simple Words)

An admin will:

1. Prepare an Excel file with product data.
2. Upload it via an API endpoint.
3. The backend will:

   * Read the file.
   * Validate columns.
   * Insert rows into PostgreSQL.
4. The AI system will now use this data.

---

## 3. Important: What You Must NOT Touch

Do NOT modify:

* Anything inside `app/ai/`
* Negotiation logic
* LLM files
* Frontend
* Existing APIs

This task is **isolated to a new admin endpoint only**.

---

## 4. Required Libraries

Install these libraries:

```bash
pip install pandas openpyxl
```

These are used to read Excel/CSV files.

---

## 5. Product Table Structure (Important)

The product table is defined in:

```
app/models/product.py
```

It has these fields:

| Column               | Meaning                   |
| -------------------- | ------------------------- |
| name                 | Product name              |
| category             | Product category          |
| base_price           | Starting price            |
| floor_price          | Minimum allowed price     |
| max_discount_percent | Max discount AI can offer |
| unit                 | Unit (kg, ton, bag, etc.) |

---

## 6. Excel File Format

The Excel file **must contain exactly these columns**:

| name | category | base_price | floor_price | max_discount_percent | unit |

Example:

| name    | category | base_price | floor_price | max_discount_percent | unit |
| ------- | -------- | ---------- | ----------- | -------------------- | ---- |
| Wheat A | Grain    | 100        | 80          | 20                   | kg   |
| Rice B  | Grain    | 200        | 160         | 15                   | kg   |

Save file as:

* `products.xlsx` or
* `products.csv`

---

## 7. Create New Admin API File

Create a new file:

```
app/api/admin_products.py
```

Paste this **exact code**:

```python
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from io import BytesIO

from app.db.session import SessionLocal
from app.models.product import Product

router = APIRouter(prefix="/admin/products", tags=["Admin Products"])

REQUIRED_COLUMNS = {
    "name",
    "category",
    "base_price",
    "floor_price",
    "max_discount_percent",
    "unit"
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_products(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()

    # Detect file type
    if file.filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(contents))
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(BytesIO(contents))
    else:
        raise HTTPException(400, "Only CSV or XLSX files are allowed")

    # Validate required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise HTTPException(
            400,
            f"Missing required columns: {missing}"
        )

    inserted = 0

    for _, row in df.iterrows():
        product = Product(
            name=str(row["name"]),
            category=str(row["category"]),
            base_price=float(row["base_price"]),
            floor_price=float(row["floor_price"]),
            max_discount_percent=float(row["max_discount_percent"]),
            unit=str(row["unit"]),
        )
        db.add(product)
        inserted += 1

    db.commit()

    return {
        "status": "success",
        "inserted_rows": inserted
    }
```

---

## 8. Register the New Router

Open file:

```
app/main.py
```

Add this import at the top:

```python
from app.api.admin_products import router as admin_products_router
```

Then add this line in the router section:

```python
app.include_router(admin_products_router)
```

Final router section should look like:

```python
app.include_router(customers_router, prefix="/customers", tags=["Customers"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(negotiations_router, tags=["Negotiations"])
app.include_router(offers_router, tags=["Offers"]) 
app.include_router(messages_router, tags=["Messages"])
app.include_router(web_sessions_router)
app.include_router(admin_products_router)
```

---

## 9. Run the Server

From project root:

```bash
uvicorn app.main:app --reload
```

You should see:

```
Database connection OK
```

---

## 10. Test the Upload (Swagger UI)

Open browser:

```
http://localhost:8000/docs
```

Find:

```
POST /admin/products/upload
```

1. Click it
2. Click "Try it out"
3. Upload Excel file
4. Click Execute

You should get:

```json
{
  "status": "success",
  "inserted_rows": 5
}
```

---

## 11. Verify Data in Database

Run SQL:

```sql
SELECT * FROM products;
```

You should see your rows.

---

## 12. Common Errors and Fixes

### Error: Missing columns

Cause: Excel headers not matching exactly.
Fix: Use exact column names.

---

### Error: Module not found

Cause: File path wrong.
Fix: Ensure file is at:

```
app/api/admin_products.py
```

---

### Error: Only CSV or XLSX allowed

Cause: File extension wrong.
Fix: Save as `.xlsx` or `.csv`.

---

## 13. Important Rules

* This endpoint is for **admin only**
* Do not expose to frontend users
* Do not delete existing products
* Do not modify AI logic

---

## 14. Final Success Criteria

This task is **complete and correct** if:

* Excel upload works in Swagger
* Data appears in `products` table
* AI negotiations still work
* No existing endpoints are broken

---

## Mental Model (For Understanding)

This feature is the **AI’s knowledge loader**.

Without this:

* AI has no business data
* Negotiation is meaningless

With this:

* Business team controls AI behavior
* System becomes production-ready

---

## Congratulations

You have implemented a **real enterprise-grade data ingestion pipeline**.

This is exactly how real AI systems receive structured business knowledge.
