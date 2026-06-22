# Real-Time E-Commerce Price Monitoring & Data Pipeline

An end-to-end data engineering pipeline designed for data analysis, featuring automated API ingestion, automated price-drop triggers, dynamic logging, and automated Excel business reporting.

## 🏗️ Project Architecture
1. **Data Ingestion (`fetch_data.py`)**: Automatically requests live items, users, and transactions from the Fake Store API.
2. **Relational Database (`database.py`)**: Cleans and stores normalized data across 4 core MySQL tables (`product`, `Customer`, `Orders`, `price_history`).
3. **Price Alert Trigger & Web Interface (`main.py`)**: Runs a FastAPI backend featuring real-time deal alerts and data access endpoints.
4. **Business Analytics (`Report.py`)**: Pulls sales data from MySQL using Pandas and aggregates metrics into an Excel reporting worksheet.

## 🛠️ Tech Stack
* **Language:** Python
* **Database:** MySQL
* **Libraries:** SQLAlchemy (ORM), PyMySQL, Pandas, FastAPI, Requests, Openpyxl

## 📊 Key Insights Captured
* Built a custom loop tracking historic price trends to trigger flags when item costs drop.
* Generated time-series sales reports mapping transaction volumes by date.