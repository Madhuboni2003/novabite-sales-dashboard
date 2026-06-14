from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import pandas as pd
import os

app = FastAPI(title="Novabite Sales Dashboard API")

# Crucial for Frontend-Backend Communication
# This prevents CORS errors when your React app tries to talk to your FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "novabite.db")

def get_db_connection():
    """Helper function to connect to our SQLite database."""
    return sqlite3.connect(DB_PATH)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Novabite Sales API! Everything is up and running."}

# -------------------------------------------------------------
# Endpoint 1: /api/products
# -------------------------------------------------------------
@app.get("/api/products")
def get_products():
    conn = get_db_connection()
    # Read the data into a Pandas DataFrame for easy grouping
    df = pd.read_sql_query("SELECT product_name, net_revenue_usd, units_sold FROM sales", conn)
    conn.close()

    # Group by product name and calculate totals
    aggregated = df.groupby("product_name").sum().reset_index()
    
    # Convert dataframe into a dictionary list format for JSON transmission
    return aggregated.to_dict(orient="records")

# -------------------------------------------------------------
# Endpoint 2: /api/summary
# -------------------------------------------------------------
@app.get("/api/summary")
def get_summary():
    conn = get_db_connection()
    df = pd.read_sql_query(
        "SELECT net_revenue_usd, gross_profit_usd, units_sold, region, channel, product_name FROM sales", 
        conn
    )
    conn.close()

    # 1. Top-level financial totals
    total_net_revenue = float(df["net_revenue_usd"].sum())
    total_gross_profit = float(df["gross_profit_usd"].sum())
    total_units_sold = int(df["units_sold"].sum())

    # 2. Gross Profit Margin % calculation
    # Formula: (Total Gross Profit / Total Net Revenue) * 100
    gross_profit_margin_pct = (total_gross_profit / total_net_revenue * 100) if total_net_revenue > 0 else 0

    # 3. Finding the top-performing metrics using Pandas idxmax()
    top_region = df.groupby("region")["net_revenue_usd"].sum().idxmax()
    top_channel = df.groupby("channel")["net_revenue_usd"].sum().idxmax()
    top_product = df.groupby("product_name")["net_revenue_usd"].sum().idxmax()

    return {
        "total_net_revenue": round(total_net_revenue, 2),
        "total_units": total_units_sold,
        "gross_profit_margin_pct": round(gross_profit_margin_pct, 2),
        "top_region": top_region,
        "top_channel": top_channel,
        "top_product": top_product
    }

# -------------------------------------------------------------
# Endpoint 3: /api/trends
# -------------------------------------------------------------
@app.get("/api/trends")
def get_trends():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT month, net_revenue_usd FROM sales", conn)
    conn.close()

    # Group and sum monthly revenue, sorting chronological by month string (YYYY-MM)
    trends = df.groupby("month")["net_revenue_usd"].sum().reset_index()
    trends = trends.sort_values(by="month")

    return trends.to_dict(orient="records")