import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

days_order = ["Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday", "Sunday"]

DATABASE_URL = os.environ["DATABASE_URL"]
SHEETS_URL = os.environ["GOOGLE_SHEET"]

print("Script is running")