from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Ecommerce API running 🚀"}

@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Perfume A", "price": 50},
        {"id": 2, "name": "Perfume B", "price": 70},
        {"id": 3, "name": "Perfume C", "price": 90}
    ]

orders = []

@app.post("/orders")
def create_order(order: dict):
    order_id = len(orders) + 1
    order["id"] = order_id
    orders.append(order)

    return {"order_id": order_id}

@app.get("/orders/{id}")
def get_order(id: int):
    for o in orders:
        if o["id"] == id:
            return o
    return {"error": "Not found"}

def send_email(to, subject, message):
    print(f"Email sent to {to}: {subject}")
