from fastapi import FastAPI, Depends
from pydantic import BaseModel  
from sqlalchemy.orm import Session
import database

app = FastAPI()

# This tells FastAPI exactly what fields to show on the webpage for adding a product
class ProductCreate(BaseModel):
    Product_Name: str
    Price: float
    Stock: int

# Helper tool to open/close database connections
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"Message": "E-commerce Price Tracker API is Live!"}

# ================= PRODUCTS ENDPOINTS =================
@app.post("/products")
def add_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    name = product_data.Product_Name
    price = product_data.Price
    stock = product_data.Stock

    # 1. Save it to your core product table
    new_product = database.Product(Product_Name=name, Price=price, Stock=stock)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # 2. FIX: Log this entry into your price history table too!
    history_entry = database.PriceHistory(Product_Id=new_product.Product_Id, Price=price)
    db.add(history_entry)
    db.commit()

    # 3. Check for your price trigger alert
    if name.lower() == "laptop" and price <= 45000:
        return {
            "status": "Product added AND ALERT FIRED!",
            "alert_message": f"🔥 Price Drop Alert! {name} is now only {price}!",
            "product": new_product
        }
        
    return {"status": "Product added successfully", "product": new_product}

# ================= CUSTOMERS ENDPOINTS =================
@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    return db.query(database.Customer).all()

# ================= ORDERS ENDPOINTS =================
@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return db.query(database.Order).all()

# ================= PRICE HISTORY ENDPOINTS =================
@app.get("/tracker/history")
def view_price_history(db: Session = Depends(get_db)):
    return db.query(database.PriceHistory).all()