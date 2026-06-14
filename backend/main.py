from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# Initialize configurations out of our secure environment file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(title="Novabite Sales Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "novabite.db")

# This explicitly reads the variable out of your .env file
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI SDK client but redirect it to OpenRouter's Cloud Server
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Novabite Sales API! Everything is up and running."}

@app.get("/api/products")
def get_products():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT product_name, net_revenue_usd, units_sold FROM sales", conn)
    conn.close()
    aggregated = df.groupby("product_name").sum().reset_index()
    return aggregated.to_dict(orient="records")

@app.get("/api/summary")
def get_summary():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT net_revenue_usd, gross_profit_usd, units_sold, region, channel, product_name FROM sales", conn)
    conn.close()

    total_net_revenue = float(df["net_revenue_usd"].sum())
    total_gross_profit = float(df["gross_profit_usd"].sum())
    total_units_sold = int(df["units_sold"].sum())

    gross_profit_margin_pct = (total_gross_profit / total_net_revenue * 100) if total_net_revenue > 0 else 0

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

@app.get("/api/trends")
def get_trends():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT month, net_revenue_usd FROM sales", conn)
    conn.close()
    trends = df.groupby("month")["net_revenue_usd"].sum().reset_index().sort_values(by="month")
    return trends.to_dict(orient="records")

def get_db_connection():
    return sqlite3.connect(DB_PATH)


# -------------------------------------------------------------
# Endpoint 4: /api/chat (OpenRouter Text-to-SQL Engine)
# -------------------------------------------------------------
@app.post("/api/chat")
def handle_chat(payload: ChatRequest):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="OpenRouter API key missing in local .env configuration.")

    user_question = payload.question

    db_schema_context = """
    You are an expert data analyst. Your database is SQLite with a table named 'sales'. Columns:
    - transaction_id: TEXT
    - date: TEXT (YYYY-MM-DD)
    - month: TEXT (YYYY-MM)
    - quarter: TEXT (e.g., Q1-2024)
    - sku: TEXT
    - product_name: TEXT
    - category: TEXT (Personal Care, Snacks, Beverages, Home Care)
    - subcategory: TEXT
    - region: TEXT (North, South, East, West, Central)
    - channel: TEXT (Modern Trade, General Trade, E-Commerce, Direct to Consumer)
    - sales_rep: TEXT
    - units_sold: INTEGER
    - unit_price_usd: REAL
    - gross_revenue_usd: REAL
    - discount_pct: REAL
    - net_revenue_usd: REAL
    - cogs_usd: REAL
    - gross_profit_usd: REAL
    """

    try:
        # Prompt 1: Generate purely code execution instruction block
        sql_prompt = f"""
        {db_schema_context}
        Convert this user question into a valid SQLite SELECT query: "{user_question}"
        Return ONLY the raw SQL query string. No formatting markdown, no backticks block, no descriptions.
        """
        
        sql_completion = client.chat.completions.create(
            model="openrouter/free",  # Routes automatically to free open-source models
            messages=[{"role": "user", "content": sql_prompt}],
            temperature=0.0
        )
        generated_sql = sql_completion.choices[0].message.content.strip()

        # ─── DIAGNOSTIC LOGS FOR VERIFICATION ─────────────────────────────
        print("\n[DEBUG] --- THE AI GENERATED THIS SQL QUERY ---")
        print(generated_sql, "\n")
        # ──────────────────────────────────────────────────────────────────

        # Execute the generated SQL query against our local database 
        conn = get_db_connection()
        query_result_df = pd.read_sql_query(generated_sql, conn)
        conn.close()
        
        data_summary = query_result_df.to_string(index=False)

        # Prompt 2: Summarize technical output table back into a conversational sentence
        synthesis_prompt = f"""
        A manager asked: "{user_question}"
        The internal database query execution returned this data:
        {data_summary}
        
        Provide a concise, professional answer directly responding to the manager based on this data.
        """
        
        final_completion = client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": synthesis_prompt}],
            temperature=0.2
        )
        
        return {"answer": final_completion.choices[0].message.content.strip()}

    except Exception as e:
        return {"answer": f"I encountered an error calculating that metric. Details: {str(e)}"}