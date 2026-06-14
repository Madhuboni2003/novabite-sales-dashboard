import csv
import sqlite3
import os

# Define file paths relative to this script
DB_PATH = os.path.join(os.path.dirname(__file__), "novabite.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "novabite_sales_data.csv")

def seed_database():
    print("Starting database seeding process...")

    # 1. Connect to SQLite (It will automatically create 'novabite.db' if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 2. Create the sales table matching your dataset schema exactly
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            transaction_id TEXT PRIMARY KEY,
            date TEXT,
            month TEXT,
            quarter TEXT,
            sku TEXT,
            product_name TEXT,
            category TEXT,
            subcategory TEXT,
            region TEXT,
            channel TEXT,
            sales_rep TEXT,
            units_sold INTEGER,
            unit_price_usd REAL,
            gross_revenue_usd REAL,
            discount_pct REAL,
            net_revenue_usd REAL,
            cogs_usd REAL,
            gross_profit_usd REAL
        )
    """)
    
    # Clear out old data if the script is run a second time to prevent duplicates
    cursor.execute("DELETE FROM sales")

    # 3. Open and parse the CSV file
    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return

    with open(CSV_PATH, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        
        # Prepare an insertion query
        insert_query = """
            INSERT INTO sales (
                transaction_id, date, month, quarter, sku, product_name,
                category, subcategory, region, channel, sales_rep,
                units_sold, unit_price_usd, gross_revenue_usd,
                discount_pct, net_revenue_usd, cogs_usd, gross_profit_usd
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Loop through each row in the CSV and append to a batch list
        rows_to_insert = []
        for row in csv_reader:
            rows_to_insert.append((
                row["transaction_id"],
                row["date"],
                row["month"],
                row["quarter"],
                row["sku"],
                row["product_name"],
                row["category"],
                row["subcategory"],
                row["region"],
                row["channel"],
                row["sales_rep"],
                int(row["units_sold"]),
                float(row["unit_price_usd"]),
                float(row["gross_revenue_usd"]),
                float(row["discount_pct"]),
                float(row["net_revenue_usd"]),
                float(row["cogs_usd"]),
                float(row["gross_profit_usd"])
            ))
        
        # 4. Efficiently execute all insertions in a single batch
        cursor.executemany(insert_query, rows_to_insert)
        
    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Success! Successfully seeded {len(rows_to_insert)} transaction rows into {DB_PATH}.")

if __name__ == "__main__":
    seed_database()