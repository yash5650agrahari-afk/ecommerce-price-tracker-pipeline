import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Connects directly to your Ecommerce MySQL database
DATABASE_URL = "mysql+pymysql://root:Yash%407529@localhost/Ecommerce"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 1. Maps directly to your MySQL 'product' table
class Product(Base):
    __tablename__ = "product"
    __table_args__ = {'extend_existing': True}
    
    Product_Id = Column(Integer, primary_key=True, autoincrement=True)
    Product_Name = Column(String(255))
    Price = Column(Float) 
    Stock = Column(Integer)

# 2. RESTORED: Maps directly to your MySQL 'Customer' table
class Customer(Base):
    __tablename__ = "Customer"
    __table_args__ = {'extend_existing': True}
    
    Customer_Id = Column(Integer, primary_key=True, autoincrement=True)
    Customer_Name = Column(String(255))
    Email = Column(String(255))

# 3. RESTORED: Maps directly to your MySQL 'Orders' table
class Order(Base):
    __tablename__ = "Orders"
    __table_args__ = {'extend_existing': True}
    
    Order_Id = Column(Integer, primary_key=True, autoincrement=True)
    Customer_Id = Column(Integer)
    Total_Amount = Column(Float)
    Order_Date = Column(Date)

# 4. Maps to your table that logs daily price histories over time
class PriceHistory(Base):
    __tablename__ = "price_history"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    Product_Id = Column(Integer)
    Price = Column(Float)
    Checked_At = Column(DateTime, default=datetime.utcnow)

# This ensuring all tables are perfectly synced and built in MySQL
Base.metadata.create_all(bind=engine)