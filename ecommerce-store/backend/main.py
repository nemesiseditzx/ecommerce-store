from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Ecommerce API running 🚀"}

@app.get("/products")
def get_products():
    return [
        {"id": 1, "name": "Perfume A", "price": 50},
        {"id": 2, "name": "Perfume B", "price": 70}
    ]