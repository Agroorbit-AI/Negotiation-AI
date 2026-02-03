from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

from app.api.customers import router as customers_router
from app.api.products import router as products_router
from app.api.negotiations import router as negotiations_router
from app.api.messages import router as messages_router
from app.api.offers import router as offers_router   # ✅ Placeholder for future phase 2
from app.api.web_sessions import router as web_sessions_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Agro Negotiation API",
    version="1.0.0",
    description="Production backend for AI-based B2B Agro Product Negotiation System",
)
# ------------------------
# Web call
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Startup DB check
# ------------------------
@app.on_event("startup")
def startup_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection OK")
    except Exception as e:
        print("❌ Database connection failed:", e)
        raise e

# ------------------------
# Health check
# ------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------
# Routers
# ------------------------
app.include_router(customers_router, prefix="/customers", tags=["Customers"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(negotiations_router, tags=["Negotiations"])
app.include_router(offers_router, tags=["Offers"]) 
app.include_router(messages_router, tags=["Messages"])
app.include_router(web_sessions_router)
