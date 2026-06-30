import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

days_order = ["Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday"]

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
#SHEETS_URL = os.environ["GOOGLE_SHEET"]

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    df = pd.read_sql(text("""
        SELECT w.*, p.category, p.core
        FROM daily_waste w
        LEFT JOIN pastries p ON w.name = p.name
    """), conn)

df["date"] = pd.to_datetime(df["date"])
df["day"] =  pd.Categorical(df["date"].dt.day_name(), categories=days_order, ordered=True)
df["week_num"] = (df["date"] - df["date"].min()).dt.days //7 + 1

print(df)