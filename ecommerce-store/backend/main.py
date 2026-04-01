from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import stripe
from config import STRIPE_SECRET_KEY, FRONTEND_URL

app = FastAPI()

stripe.api_key = STRIPE_SECRET_KEY

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- PRODUCTS ----------------
@app.get("/products")
def products():
    return [
        {"id": 1, "name": "Perfume A", "price": 50},
        {"id": 2, "name": "Perfume B", "price": 70},
        {"id": 3, "name": "Perfume C", "price": 90}
    ]

# ---------------- ORDERS ----------------
orders = []

@app.post("/orders")
def create(order: dict):
    order_id = len(orders) + 1
    order["id"] = order_id
    order["order_status"] = "pending"
    order["payment_status"] = "unpaid"
    orders.append(order)
    return {"order_id": order_id}

@app.get("/orders")
def all_orders():
    return orders

@app.get("/orders/{id}")
def one(id: int):
    for o in orders:
        if o["id"] == id:
            return o
    return {"error": "not found"}

@app.put("/orders/{id}")
def update(id: int, status: str):
    for o in orders:
        if o["id"] == id:
            o["order_status"] = status
            return {"message": "updated"}
    return {"error": "not found"}

# ---------------- STRIPE ----------------
@app.post("/checkout")
def checkout(order: dict):

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "Order Payment"},
                "unit_amount": int(order["total"] * 100),
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=f"{https://ecommerce-store-coral-alpha.vercel.app/}/track.html",
        cancel_url=f"{https://ecommerce-store-coral-alpha.vercel.app/}/",
    )

    return {"url": session.url}
