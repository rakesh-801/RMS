# test_connection.py
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
print("🔗 Testing PostgreSQL connection...",os.getenv("DATABASE_URL"))

try:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    print("✅ PostgreSQL connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")