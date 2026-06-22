import requests
import random
from sqlalchemy.orm import Session
import database

def run_pipeline():
    db: Session = database.SessionLocal()
    
    # ================= 1. FETCH & SYNC PRODUCTS =================
    print("🔄 Fetching live products from Fake Store API...")
    try:
        prod_response = requests.get("https://fakestoreapi.com/products").json()
        print(f"📦 Found {len(prod_response)} products. Syncing...")
        for item in prod_response:
            p_id = item["id"]
            p_name = item["title"]
            current_price = float(item["price"])

            existing_product = db.query(database.Product).filter(database.Product.Product_Id == p_id).first()
            if existing_product:
                old_price = existing_product.Price
                if current_price < old_price:
                    savings = old_price - current_price
                    print(f"🔥 PRICE ALERT: '{p_name}' dropped by ${savings:.2f}!")
                existing_product.Price = current_price
            else:
                new_product = database.Product(Product_Id=p_id, Product_Name=p_name, Price=current_price)
                db.add(new_product)
            
            # Log history
            history_entry = database.PriceHistory(Product_Id=p_id, Price=current_price)
            db.add(history_entry)
    except Exception as e:
        print(f"❌ Product Sync Failed: {e}")

    # ================= 2. FETCH & SYNC CUSTOMERS =================
    print("\n🔄 Fetching live users from Fake Store API...")
    try:
        user_response = requests.get("https://fakestoreapi.com/users").json()
        print(f"👥 Found {len(user_response)} users. Syncing...")
        for user in user_response:
            u_id = user["id"]
            # Combine firstname and lastname for your Customer_Name column
            first_name = user["name"]["firstname"].capitalize()
            last_name = user["name"]["lastname"].capitalize()
            full_name = f"{first_name} {last_name}"
            email = user["email"]

            existing_customer = db.query(database.Customer).filter(database.Customer.Customer_Id == u_id).first()
            if not existing_customer:
                new_customer = database.Customer(Customer_Id=u_id, Customer_Name=full_name, Email=email)
                db.add(new_customer)
    except Exception as e:
        print(f"❌ Customer Sync Failed: {e}")

    # ================= 3. FETCH & SYNC ORDERS =================
    print("\n🔄 Fetching live carts (orders) from Fake Store API...")
    try:
        cart_response = requests.get("https://fakestoreapi.com/carts").json()
        print(f"🛒 Found {len(cart_response)} carts. Syncing...")
        for cart in cart_response:
            o_id = cart["id"]
            c_id = cart["userId"]
            # Format the date string correctly (YYYY-MM-DD)
            order_date = cart["date"].split("T")[0]
            
            # The Fake Store API doesn't include prices in carts, so we generate a realistic random total amount
            random_total = round(random.uniform(500.0, 15000.0), 2)

            existing_order = db.query(database.Order).filter(database.Order.Order_Id == o_id).first()
            if not existing_order:
                new_order = database.Order(
                    Order_Id=o_id,
                    Customer_Id=c_id,
                    Total_Amount=random_total,
                    Order_Date=order_date
                )
                db.add(new_order)
    except Exception as e:
        print(f"❌ Orders Sync Failed: {e}")

    # Save everything cleanly to MySQL
    db.commit()
    db.close()
    print("\n✅ All tables (Products, Customers, Orders) successfully synced with Fake Store data!")

if __name__ == "__main__":
    run_pipeline()