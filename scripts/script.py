import os
#from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

days_order = ["Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday"]

#load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
SHEETS_URL = os.environ["GOOGLE_SHEET"]

engine = create_engine(DATABASE_URL)

df_gs = pd.read_csv(SHEETS_URL)
print(df_gs)

df_gs.to_sql("test_daily_waste", engine, if_exists="append", index=False)

with engine.connect() as conn:
    df = pd.read_sql(text("""
        SELECT w.*, p.category, p.core
        FROM daily_waste w
        LEFT JOIN pastries p ON w.name = p.name
        ORDER BY date ASC
    """), conn)

df['date'] = pd.to_datetime(df['date'])
df['day'] =  pd.Categorical(df['date'].dt.day_name(), categories=days_order, ordered=True)
df['week_num'] = (df['date'] - df['date'].min()).dt.days //7 + 1

avg_day = (
    df.groupby(["date", "day"])["waste"].sum()
    .reset_index()
    .groupby("day")["waste"].mean()
    .reset_index()
)
print(avg_day)

with engine.begin() as conn:
    for _, row in avg_day.iterrows():
        conn.execute(text("""
            UPDATE avg_day
            SET waste = :waste
            WHERE day = :day
            """), {"day": row.day, "waste": row.waste}
        )

print(df)