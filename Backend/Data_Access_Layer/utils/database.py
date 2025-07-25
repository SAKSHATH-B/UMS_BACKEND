from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ...config.env_loader import get_env_var
 
DB_USER = get_env_var("DB_USER")
DB_PASSWORD = get_env_var("DB_PASSWORD")
DB_PORT = get_env_var("DB_PORT")
DB_NAME = get_env_var("DB_NAME")
DB_DRIVER = get_env_var("DB_DRIVER")
DB_HOST = get_env_var("DB_HOST") 


 
DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print("DB_URL:", DB_URL)  # Debugging line to check the DB_URL
 
# ✅ Move pool_pre_ping here
engine = create_engine(DB_URL, pool_pre_ping=True)
 
# ✅ No pool_pre_ping here
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()
 