from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Hardcode or use env vars properly here
DB_URL = "mysql+pymysql://root:1234@localhost:3306/User_Management"

try:
    engine = create_engine(DB_URL, pool_pre_ping=True)
    with engine.connect() as conn:
        print("✅ Connected to DB successfully")
except Exception as e:
    print("❌ Connection failed:", e)
    import traceback
    traceback.print_exc()
